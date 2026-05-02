"""Async review system — LLM flags items needing human judgment.

During ingest, the LLM can flag:
  - Uncertain claims
  - Contradictions with existing pages
  - Low-confidence extractions
  - Ambiguous entities

Each review item has:
  - Predefined actions (approve, reject, merge, edit)
  - Pre-generated search queries for verification
  - Priority level (low/medium/high)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


REVIEW_ACTIONS = {
    "approve": "Accept the content as-is",
    "reject": "Remove the flagged content",
    "merge": "Merge with an existing page",
    "edit": "Manual edit needed",
    "verify": "Verify via web search",
    "split": "Split into multiple pages",
}


class ReviewSystem:
    """Track and manage review items flagged during ingest."""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.review_file = self.project_path / ".llm-wiki" / "review-queue.json"

    def add_review(
        self,
        item_type: str,
        page_slug: str,
        reason: str,
        priority: str = "medium",
        suggested_action: str = "verify",
        search_queries: List[str] | None = None,
        details: dict | None = None,
    ) -> dict:
        """Add a review item.

        Args:
            item_type: "uncertain_claim", "contradiction", "low_confidence", "ambiguous_entity", "duplicate"
            page_slug: The wiki page this relates to
            reason: Why it needs review
            priority: "low", "medium", "high"
            suggested_action: One of REVIEW_ACTIONS keys
            search_queries: Pre-generated queries for verification
            details: Additional context
        """
        item = {
            "id": f"rev-{datetime.now().strftime('%Y%m%d%H%M%S')}-{page_slug[:20]}",
            "type": item_type,
            "page_slug": page_slug,
            "reason": reason,
            "priority": priority,
            "status": "pending",
            "suggested_action": suggested_action,
            "search_queries": search_queries or [],
            "details": details or {},
            "created_at": datetime.now().isoformat(),
        }
        queue = self._load()
        queue.append(item)
        self._save(queue)
        return item

    def get_pending(self, priority: str | None = None) -> List[dict]:
        """Get pending review items, optionally filtered by priority."""
        items = [i for i in self._load() if i["status"] == "pending"]
        if priority:
            items = [i for i in items if i["priority"] == priority]
        items.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x["priority"], 1))
        return items

    def resolve(self, review_id: str, action: str, note: str = "") -> bool:
        """Resolve a review item with an action."""
        queue = self._load()
        for item in queue:
            if item["id"] == review_id:
                item["status"] = "resolved"
                item["resolved_action"] = action
                item["resolved_note"] = note
                item["resolved_at"] = datetime.now().isoformat()
                self._save(queue)
                return True
        return False

    def dismiss(self, review_id: str) -> bool:
        """Dismiss a review item without action."""
        queue = self._load()
        for item in queue:
            if item["id"] == review_id:
                item["status"] = "dismissed"
                item["resolved_at"] = datetime.now().isoformat()
                self._save(queue)
                return True
        return False

    def get_stats(self) -> dict:
        """Get review queue statistics."""
        queue = self._load()
        return {
            "total": len(queue),
            "pending": sum(1 for i in queue if i["status"] == "pending"),
            "resolved": sum(1 for i in queue if i["status"] == "resolved"),
            "dismissed": sum(1 for i in queue if i["status"] == "dismissed"),
            "by_priority": {
                "high": sum(1 for i in queue if i["priority"] == "high" and i["status"] == "pending"),
                "medium": sum(1 for i in queue if i["priority"] == "medium" and i["status"] == "pending"),
                "low": sum(1 for i in queue if i["priority"] == "low" and i["status"] == "pending"),
            },
            "by_type": {
                t: sum(1 for i in queue if i["type"] == t and i["status"] == "pending")
                for t in {i["type"] for i in queue if i["status"] == "pending"}
            },
        }

    def flag_ingest_items(self, analysis: dict, page_slug: str) -> List[dict]:
        """Auto-flag items from LLM analysis that need review.

        Called after ingest to flag low-confidence extractions.
        """
        flagged = []

        confidence = analysis.get("confidence", 1.0)
        if isinstance(confidence, str):
            try:
                confidence = float(confidence)
            except ValueError:
                confidence = 0.5

        if confidence < 0.5:
            flagged.append(self.add_review(
                item_type="low_confidence",
                page_slug=page_slug,
                reason=f"Low confidence extraction ({confidence}). Content may need verification.",
                priority="high",
                suggested_action="verify",
                search_queries=analysis.get("suggested_searches", []),
            ))

        for entity in analysis.get("entities", []):
            if entity.get("ambiguous", False):
                flagged.append(self.add_review(
                    item_type="ambiguous_entity",
                    page_slug=page_slug,
                    reason=f"Ambiguous entity: {entity.get('name', 'unknown')}. May match existing pages.",
                    priority="medium",
                    suggested_action="merge",
                    search_queries=[f"{entity.get('name', '')} wiki"],
                ))

        return flagged

    def _load(self) -> List[dict]:
        if self.review_file.exists():
            try:
                return json.loads(self.review_file.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    def _save(self, queue: List[dict]) -> None:
        self.review_file.parent.mkdir(parents=True, exist_ok=True)
        self.review_file.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")
