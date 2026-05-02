"""SHA256-based ingest cache to skip unchanged files."""

import hashlib
import json
import os
from pathlib import Path


class IngestCache:
    """Cache that tracks ingested files by their SHA256 content hash."""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.cache_dir = self.project_path / ".llm-wiki"
        self.cache_file = self.cache_dir / "ingest-cache.json"
        self._data: dict = {}
        self._load()

    def _load(self):
        if self.cache_file.exists():
            try:
                self._data = json.loads(self.cache_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                self._data = {}

    def _save(self):
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file.write_text(
            json.dumps(self._data, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    @staticmethod
    def _hash(content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def check(self, filename: str, content: str) -> list[str] | None:
        """Return cached output paths if content unchanged, else None."""
        h = self._hash(content)
        entry = self._data.get(filename)
        if entry and entry.get("hash") == h:
            return entry.get("output_paths", [])
        return None

    def save(self, filename: str, content: str, output_paths: list[str]):
        """Save cache entry for a file."""
        self._data[filename] = {
            "hash": self._hash(content),
            "output_paths": output_paths,
        }
        self._save()

    def invalidate(self, filename: str):
        """Remove a cache entry."""
        self._data.pop(filename, None)
        self._save()

    def clear(self):
        """Clear all cache entries."""
        self._data = {}
        self._save()
