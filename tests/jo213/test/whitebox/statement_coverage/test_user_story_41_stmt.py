# Test file for User Story 41
# Testing Type: whitebox
# Technique: statement_coverage
# Team Member: jo213
# Original file: test_user_story_41.py

from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
import pytest
from vca.storage.history_store import HistoryStore
def _fixed_now():
    return datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

def test_us41_permission_error_does_not_crash_save(
    tmp_path: Path, monkeypatch, caplog
) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, now_utc=_fixed_now)

    original_open = Path.open

    def boom(self: Path, *args, **kwargs):
        mode = args[0] if args else kwargs.get("mode", "")
        if isinstance(mode, str) and ("a" in mode or "w" in mode):
            raise PermissionError("nope")
        return original_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", boom)

    with caplog.at_level("ERROR"):
        store.save_turn("u", "a")

    assert any("History save failed" in rec.message for rec in caplog.records)

def test_us41_atomic_rewrite_failure_does_not_corrupt_existing_file(
    tmp_path: Path, monkeypatch
) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, max_turns=1, now_utc=_fixed_now)

    store.save_turn("u1", "a1")
    before = p.read_text(encoding="utf-8")

    # Force the atomic replace step to fail
    def replace_boom(self: Path, target: Path):
        raise OSError("replace failed")

    monkeypatch.setattr(Path, "replace", replace_boom, raising=True)

    # This calls _atomic_rewrite_lines under the hood
    store._trim_file_to_last_n_turns(1)

    after = p.read_text(encoding="utf-8")
    assert after == before

def test_us41_trim_permission_error_does_not_crash(
    tmp_path: Path, monkeypatch, caplog
) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, max_turns=1, now_utc=_fixed_now)
    store.save_turn("u1", "a1")

    # fail tmp file creation to simulate IO failure during trim
    import tempfile as _tempfile

    def mkstemp_boom(*args, **kwargs):
        raise OSError("mkstemp failed")

    monkeypatch.setattr(_tempfile, "mkstemp", mkstemp_boom, raising=True)

    with caplog.at_level("ERROR"):
        store._trim_file_to_last_n_turns(1)

    # Should not crash, and should log failure
    assert any("History atomic rewrite failed" in rec.message for rec in caplog.records)
