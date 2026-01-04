# Test file for User Story 35
# Testing Type: whitebox
# Technique: statement_coverage
# Team Member: sa1068
# Original file: test_user_story_35.py

from __future__ import annotations
from pathlib import Path
from vca.storage.history_store import HistoryStore


def _write_turns_jsonl(path: Path, turns: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    for i in range(turns):
        lines.append(f'{{"ts":"t{i}u","role":"user","content":"u{i}"}}')
        lines.append(f'{{"ts":"t{i}a","role":"assistant","content":"a{i}"}}')
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_user_story_35_history_load_turns_uses_bounded_stream(
    tmp_path: Path, monkeypatch
) -> None:
    p = tmp_path / "history.jsonl"
    _write_turns_jsonl(p, turns=50)

    store = HistoryStore(p, max_turns=50)

    called = {"all": 0, "last": 0}

    original_all = HistoryStore._stream_all_lines
    original_last = HistoryStore._stream_last_lines

    def spy_all(self) -> list[str]:
        called["all"] += 1
        return original_all(self)

    def spy_last(self, max_lines: int) -> list[str]:
        called["last"] += 1
        return original_last(self, max_lines=max_lines)

    monkeypatch.setattr(HistoryStore, "_stream_all_lines", spy_all, raising=True)
    monkeypatch.setattr(HistoryStore, "_stream_last_lines", spy_last, raising=True)

    turns = store.load_turns(max_turns=5)
    assert len(turns) == 5
    assert called["last"] >= 1
    assert called["all"] == 0


def test_user_story_35_history_trim_does_not_read_full_file_for_jsonl(
    tmp_path: Path, monkeypatch
) -> None:
    p = tmp_path / "history.jsonl"
    _write_turns_jsonl(p, turns=30)

    store = HistoryStore(p, max_turns=10)

    def explode(*args, **kwargs):
        raise AssertionError(
            "load_history should not be used for jsonl trimming in user story 35"
        )

    monkeypatch.setattr(HistoryStore, "load_history", explode, raising=True)

    store.save_turn("new user", "new assistant")

    turns = store.load_turns(max_turns=10)
    assert len(turns) == 10
