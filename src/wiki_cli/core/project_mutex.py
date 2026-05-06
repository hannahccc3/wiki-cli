"""
Per-project async mutex using filelock.

Prevents concurrent ingest calls for the same project from racing
on wiki/index.md — each caller takes turns rather than overwriting
each other's index updates.

Usage:
    from wiki_cli.core.project_mutex import ProjectLock

    with ProjectLock(project_path):
        engine.ingest(source_path)
"""
from pathlib import Path
from filelock import FileLock


class ProjectLock:
    """Context manager that serializes work on a per-project basis.

    Uses FileLock (cross-platform, process-level) under the hood.
    The lock file lives at `<project>/.llm-wiki/.project.lock`.
    """

    def __init__(self, project_path: str | Path, timeout: float = 300.0):
        self.project_path = Path(project_path)
        lock_dir = self.project_path / ".llm-wiki"
        lock_dir.mkdir(parents=True, exist_ok=True)
        self.lock_path = lock_dir / ".project.lock"
        self.timeout = timeout
        self._lock = FileLock(str(self.lock_path), timeout=timeout)

    def __enter__(self) -> "ProjectLock":
        self._lock.acquire(timeout=self.timeout)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._lock.release()
