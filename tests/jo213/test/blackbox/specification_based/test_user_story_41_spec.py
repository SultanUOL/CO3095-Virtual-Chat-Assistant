# Test file for User Story 41
# Testing Type: blackbox
# Technique: specification_based
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


def test_us41_missing_history_file_starts_empty(tmp_path: Path) -> None:
    store = HistoryStore(path=tmp_path / "missing.jsonl", now_utc=_fixed_now)
    assert store.load_turns() == []


def test_us41_append_uses_newlines_and_two_records(tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, now_utc=_fixed_now)
    store.save_turn("hi", "hello")

    text = p.read_text(encoding="utf-8")
    assert text.endswith("\n")

    lines = [ln for ln in text.splitlines() if ln.strip()]
    assert len(lines) == 2

    r0 = json.loads(lines[0])
    r1 = json.loads(lines[1])
    assert r0["role"] == "user"
    assert r1["role"] == "assistant"


def test_us41_trimming_keeps_last_n_turns(tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, max_turns=2, now_utc=_fixed_now)

    store.save_turn("u1", "a1")
    store.save_turn("u2", "a2")
    store.save_turn("u3", "a3")

    turns = store.load_turns()
    assert [t.user_text for t in turns] == ["u2", "u3"]
    assert [t.assistant_text for t in turns] == ["a2", "a3"]


def test_us41_detects_corrupted_records_without_crashing(
    tmp_path: Path, caplog
) -> None:
    # Keep behaviour consistent with earlier story: corruption -> empty + log
    p = tmp_path / "history.jsonl"
    p.write_text(
        '{"ts":"x","role":"user","content":"hi"}\nNOT JSON\n', encoding="utf-8"
    )

    store = HistoryStore(path=p)

    with caplog.at_level("ERROR"):
        turns = store.load_turns()

    assert turns == []
    assert any("History file is corrupted" in rec.message for rec in caplog.records)


@pytest.mark.parametrize(
    "content,should_log_corruption",
    [
        (
            '{"ts":"x","role":"user","content":"hi"}\n{"ts":"x","role":"assistant","content":"ok"}\n',
            False,
        ),  # t0
        ("   \n", False),  # t1 (blank) => fine, no corruption log required
        (
            '{"ts":"x","role":"user","content":"hi"}\n{"role":\n',
            True,
        ),  # t2 invalid JSON => corruption
        ("123\n", True),  # t3 non-dict JSON => corruption
        (
            '{"ts":"x","role":"system","content":"x"}\n',
            True,
        ),  # t4 invalid role => corruption
    ],
)
def test_us41_symbolic_concolic_paths(
    tmp_path: Path, caplog, content: str, should_log_corruption: bool
) -> None:
    p = tmp_path / "history.jsonl"
    p.write_text(content, encoding="utf-8")

    store = HistoryStore(path=p)

    with caplog.at_level("ERROR"):
        turns = store.load_turns()

    # For t0, should load one turn; otherwise, safe fallback is empty.
    if not should_log_corruption and "assistant" in content:
        assert len(turns) == 1
        assert turns[0].user_text == "hi"
        assert turns[0].assistant_text == "ok"
    else:
        assert turns == []

    if should_log_corruption:
        assert any("History file is corrupted" in rec.message for rec in caplog.records)
