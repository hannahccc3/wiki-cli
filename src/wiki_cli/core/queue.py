"""Persistent ingest queue with crash recovery.

Features:
  - Serial processing of ingest jobs
  - Crash recovery: resumes from last checkpoint
  - Cancel / retry support
  - Progress tracking (JSON-based)
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class IngestQueue:
    """File-based persistent queue for document ingestion."""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.queue_file = self.project_path / ".llm-wiki" / "ingest-queue.json"
        self.progress_file = self.project_path / ".llm-wiki" / "ingest-progress.json"

    def enqueue(self, source_path: str, collection: str | None = None) -> None:
        """Add a source to the ingest queue."""
        queue = self._load_queue()
        queue.append({
            "source": str(source_path),
            "collection": collection,
            "status": "pending",
            "added_at": datetime.now().isoformat(),
        })
        self._save_queue(queue)

    def enqueue_batch(self, source_paths: List[str], collection: str | None = None) -> int:
        """Add multiple sources. Returns count added."""
        queue = self._load_queue()
        existing = {item["source"] for item in queue}
        added = 0
        for path in source_paths:
            if str(path) not in existing:
                queue.append({
                    "source": str(path),
                    "collection": collection,
                    "status": "pending",
                    "added_at": datetime.now().isoformat(),
                })
                added += 1
        self._save_queue(queue)
        return added

    def get_pending(self) -> List[dict]:
        """Get all pending items."""
        return [item for item in self._load_queue() if item["status"] == "pending"]

    def get_progress(self) -> dict:
        """Get current progress summary."""
        queue = self._load_queue()
        progress = self._load_progress()
        total = len(queue)
        done = sum(1 for item in queue if item["status"] == "done")
        failed = sum(1 for item in queue if item["status"] == "failed")
        pending = sum(1 for item in queue if item["status"] == "pending")
        processing = progress.get("current")

        return {
            "total": total,
            "done": done,
            "failed": failed,
            "pending": pending,
            "current": processing,
            "progress_pct": round(done / total * 100, 1) if total > 0 else 0,
        }

    def mark_processing(self, source: str) -> None:
        """Mark an item as currently being processed."""
        self._save_progress({"current": source, "started_at": datetime.now().isoformat()})
        queue = self._load_queue()
        for item in queue:
            if item["source"] == source and item["status"] == "pending":
                item["status"] = "processing"
                break
        self._save_queue(queue)

    def mark_done(self, source: str, output_paths: list[str] | None = None) -> None:
        """Mark an item as successfully processed."""
        queue = self._load_queue()
        for item in queue:
            if item["source"] == source:
                item["status"] = "done"
                item["completed_at"] = datetime.now().isoformat()
                if output_paths:
                    item["output_paths"] = output_paths
                break
        self._save_queue(queue)
        self._save_progress({"current": None})

    def mark_failed(self, source: str, error: str = "") -> None:
        """Mark an item as failed."""
        queue = self._load_queue()
        for item in queue:
            if item["source"] == source:
                item["status"] = "failed"
                item["error"] = error
                item["failed_at"] = datetime.now().isoformat()
                break
        self._save_queue(queue)
        self._save_progress({"current": None})

    def retry_failed(self) -> int:
        """Reset all failed items to pending. Returns count reset."""
        queue = self._load_queue()
        count = 0
        for item in queue:
            if item["status"] == "failed":
                item["status"] = "pending"
                item.pop("error", None)
                item.pop("failed_at", None)
                count += 1
        self._save_queue(queue)
        return count

    def clear_completed(self) -> int:
        """Remove completed items from queue. Returns count removed."""
        queue = self._load_queue()
        remaining = [item for item in queue if item["status"] != "done"]
        self._save_queue(remaining)
        return len(queue) - len(remaining)

    def recover(self) -> Optional[str]:
        """Recover from crash: if an item was 'processing', reset to 'pending'.

        Returns the source path that was interrupted, or None.
        """
        progress = self._load_progress()
        current = progress.get("current")
        if not current:
            return None

        queue = self._load_queue()
        for item in queue:
            if item["source"] == current and item["status"] == "processing":
                item["status"] = "pending"
                item["recovered"] = True
                self._save_queue(queue)
                self._save_progress({"current": None})
                return current
        return None

    def _load_queue(self) -> List[dict]:
        if self.queue_file.exists():
            try:
                return json.loads(self.queue_file.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    def _save_queue(self, queue: List[dict]) -> None:
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        self.queue_file.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")

    def _load_progress(self) -> dict:
        if self.progress_file.exists():
            try:
                return json.loads(self.progress_file.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    def _save_progress(self, progress: dict) -> None:
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        self.progress_file.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding="utf-8")
