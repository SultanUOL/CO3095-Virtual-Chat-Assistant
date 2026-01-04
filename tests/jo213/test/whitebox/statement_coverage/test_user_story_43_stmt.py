# Test file for User Story 43
# Testing Type: whitebox
# Technique: statement_coverage
# Team Member: jo213
# Original file: test_user_story_43.py

from pathlib import Path
from vca.storage.history_store import HistoryStore
from vca.storage.file_lock import FileLockTimeout


def test_us43_write_locked_fails_safely_and_logs_warning(
    tmp_path: Path, monkeypatch, caplog
) -> None:
    """
    AC2: If the file is locked, the system retries briefly or fails safely with a logged warning.
    We simulate lock acquisition failure and assert save_turn does not crash and logs a warning.
    """
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, max_turns=10)

    # Make the lock acquisition fail inside the context manager.
    monkeypatch.setattr(
        "vca.storage.history_store.FileLock.acquire",
        lambda self: (_ for _ in ()).throw(FileLockTimeout("locked")),
    )

    store.save_turn("u1", "a1")  # should not crash

    assert any("file_locked=True" in r.message for r in caplog.records)


def test_us43_read_locked_returns_last_known_good(
    tmp_path: Path, monkeypatch, caplog
) -> None:
    """
    AC3: Reads during writes do not crash and return a consistent result (last known good).
    We first create a valid history (populating last_good), then simulate locked read.
    """
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, max_turns=10)

    store.save_turn("u1", "a1")
    good = store.load_turns()
    assert len(good) == 1

    # Simulate the read lock being held by another writer
    monkeypatch.setattr(
        "vca.storage.history_store.FileLock.try_acquire", lambda self: False
    )

    turns = store.load_turns()
    assert turns == good
    assert any("served from cache" in r.message for r in caplog.records)


def test_us43_write_retries_then_succeeds(tmp_path: Path, monkeypatch) -> None:
    """
    AC1: Prevent simultaneous writes corrupting the file using a simple locking strategy.
    AC2: If locked, retry briefly.
    We simulate try_acquire failing twice then succeeding; save should eventually work.
    """
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, max_turns=10)

    state = {"n": 0}

    def try_acquire(self):
        state["n"] += 1
        return state["n"] >= 3  # succeed on 3rd attempt

    monkeypatch.setattr("vca.storage.file_lock.FileLock.try_acquire", try_acquire)

    store.save_turn("u1", "a1")
    turns = store.load_turns()
    assert len(turns) == 1
    assert turns[0].user_text == "u1"
