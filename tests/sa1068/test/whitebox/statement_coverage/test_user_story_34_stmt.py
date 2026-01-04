# Test file for User Story 34
# Testing Type: whitebox
# Technique: statement_coverage
# Team Member: sa1068
# Original file: test_user_story_34.py

from __future__ import annotations
from pathlib import Path
from vca.storage.history_store import HistoryStore


def test_user_story_34_history_store_does_not_crash_on_save_open_error(
    monkeypatch, tmp_path: Path
) -> None:
    store = HistoryStore(tmp_path / "history.jsonl")

    def bad_open(*args, **kwargs):
        raise OSError("disk error")

    monkeypatch.setattr(Path, "open", bad_open, raising=True)

    store.save_turn("hi", "hello")


def test_user_story_34_history_store_does_not_crash_on_load_open_error(
    monkeypatch, tmp_path: Path
) -> None:
    p = tmp_path / "history.jsonl"
    p.write_text('{"ts":"x","role":"user","content":"a"}\n', encoding="utf-8")
    store = HistoryStore(p)

    def bad_open(*args, **kwargs):
        raise OSError("read error")

    monkeypatch.setattr(Path, "open", bad_open, raising=True)

    turns = store.load_turns()
    assert turns == []
