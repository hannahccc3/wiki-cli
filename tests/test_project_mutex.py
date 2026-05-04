"""Tests for ProjectLock (per-project concurrency control)."""
import pytest
import sys
import os
import threading
import time
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from wiki_cli.core.project_mutex import ProjectLock


class TestProjectLock:
    """ProjectLock must serialize concurrent access to the same project."""

    def test_basic_context_manager(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with ProjectLock(tmpdir):
                pass  # no-op, should not raise

    def test_serial_execution(self):
        """Two threads with the SAME project must not overlap."""
        with tempfile.TemporaryDirectory() as tmpdir:
            events = []

            def task1():
                with ProjectLock(tmpdir):
                    events.append("t1_start")
                    time.sleep(0.2)
                    events.append("t1_end")

            def task2():
                # Wait for t1 to start before entering lock
                time.sleep(0.05)
                with ProjectLock(tmpdir):
                    events.append("t2_start")
                    time.sleep(0.1)
                    events.append("t2_end")

            t1 = threading.Thread(target=task1)
            t2 = threading.Thread(target=task2)
            t2.start()
            t1.start()
            t1.join()
            t2.join()

            # Verify serialization: t1_end must come before t2_start
            assert events.index("t1_end") < events.index("t2_start"), \
                f"Expected serial execution, got: {events}"

    def test_independent_projects_can_run_concurrently(self):
        """Two threads with DIFFERENT projects must NOT wait for each other."""
        with tempfile.TemporaryDirectory() as tmpdir1, tempfile.TemporaryDirectory() as tmpdir2:
            t1_start_time = None
            t2_start_time = None
            lock = threading.Lock()

            def task1():
                nonlocal t1_start_time
                with ProjectLock(tmpdir1):
                    t1_start_time = time.time()
                    time.sleep(0.3)

            def task2():
                nonlocal t2_start_time
                time.sleep(0.05)  # stagger
                with ProjectLock(tmpdir2):
                    t2_start_time = time.time()

            t1 = threading.Thread(target=task1)
            t2 = threading.Thread(target=task2)
            t2.start()
            t1.start()
            t1.join()
            t2.join()

            # t2 should start before t1 finishes (concurrent across different projects)
            assert t2_start_time < t1_start_time + 0.3, \
                f"Expected concurrent execution for different projects, got gap: {t1_start_time + 0.3 - t2_start_time}"

    def test_exception_releases_lock(self):
        """If fn() raises, the lock must still be released."""
        with tempfile.TemporaryDirectory() as tmpdir:
            class CustomError(Exception):
                pass

            raised = False
            with tempfile.TemporaryDirectory() as tmpdir2:
                def task1():
                    nonlocal raised
                    try:
                        with ProjectLock(tmpdir):
                            raise CustomError("boom")
                    except CustomError:
                        raised = True

                def task2():
                    with ProjectLock(tmpdir):
                        time.sleep(0.2)

                t1 = threading.Thread(target=task1)
                t2 = threading.Thread(target=task2)
                t2.start()
                t1.start()
                t1.join()
                t2.join()

            assert raised, "First task should have raised"
            # t2 should have completed (lock was released after t1 exception)
