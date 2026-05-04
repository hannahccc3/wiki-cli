"""SHA256-based ingest cache with file-existence verification.

Cache design (nashsu/llm_wiki style):
- Keyed by source filename + content hash
- Cache hit is only returned if EVERY previously-written output file
  still exists on disk. This prevents ghost entries (stale paths where
  files were manually deleted but cache still lists them).
- Each entry stores: hash, timestamp, output_paths
"""
from pathlib import Path
import hashlib
import json
import time


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
            json.dumps(self._data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @staticmethod
    def _hash(content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def check(self, filename: str, content: str) -> list[str] | None:
        """Return cached output paths if content unchanged AND all files still exist.

        IMPORTANT: cache hit requires every output file to still be on disk.
        If any file is missing, we fall through to re-ingest rather than
        returning a stale list (which would create ghost stubs).
        """
        h = self._hash(content)
        entry = self._data.get(filename)
        if not entry or entry.get("hash") != h:
            return None

        output_paths: list[str] = entry.get("output_paths", [])
        if not output_paths:
            return None

        # Verify every output file still exists on disk
        wiki_root = self.project_path / "wiki"
        for rel_path in output_paths:
            # Handle both "entities/foo.md" and full "wiki/entities/foo.md" formats
            clean = rel_path
            if clean.startswith("wiki/"):
                clean = clean[5:]
            full_path = wiki_root / clean
            if not full_path.exists():
                # File no longer on disk — cache is stale, invalidate and re-ingest
                self.invalidate(filename)
                return None

        return output_paths

    def save(self, filename: str, content: str, output_paths: list[str]):
        """Save cache entry for a file."""
        self._data[filename] = {
            "hash": self._hash(content),
            "timestamp": time.time(),
            "output_paths": output_paths,
        }
        self._save()

    def invalidate(self, filename: str):
        """Remove a cache entry (e.g., when source is deleted or file missing)."""
        self._data.pop(filename, None)
        self._save()

    def clear(self):
        """Clear all cache entries."""
        self._data = {}
        self._save()
