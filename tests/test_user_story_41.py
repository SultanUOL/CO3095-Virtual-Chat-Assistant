from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from vca.storage.history_store import HistoryStore


def _fixed_now():
    return datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)


# -------------------------
# US41 Black-box tests
# -------------------------

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


def test_us41_detects_corrupted_records_without_crashing(tmp_path: Path, caplog) -> None:
    # Keep behaviour consistent with earlier story: corruption -> empty + log
    p = tmp_path / "history.jsonl"
    p.write_text('{"ts":"x","role":"user","content":"hi"}\nNOT JSON\n', encoding="utf-8")

    store = HistoryStore(path=p)

    with caplog.at_level("ERROR"):
        turns = store.load_turns()

    assert turns == []
    assert any("History file is corrupted" in rec.message for rec in caplog.records)


def test_us41_permission_error_does_not_crash_save(tmp_path: Path, monkeypatch, caplog) -> None:
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


# -------------------------
# US41 White-box tests
# -------------------------

def test_us41_atomic_rewrite_failure_does_not_corrupt_existing_file(tmp_path: Path, monkeypatch) -> None:
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


def test_us41_trim_permission_error_does_not_crash(tmp_path: Path, monkeypatch, caplog) -> None:
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


# -------------------------
# US41 Symbolic + Concolic (research evidence)
# -------------------------
"""
Symbolic decision nodes for parsing one JSONL line L:

N1: strip(L) == "" ?
N2: json.loads(L) succeeds ?
N3: isinstance(obj, dict) ?
N4: role in {"user","assistant"} ?

Concolic strategy:
- Start from valid concrete seed (t0),
- Negate constraints to hit each branch: whitespace (t1), invalid JSON (t2), non-dict JSON (t3), invalid role (t4).
"""

@pytest.mark.parametrize(
    "content,should_log_corruption",
    [
        ('{"ts":"x","role":"user","content":"hi"}\n{"ts":"x","role":"assistant","content":"ok"}\n', False),  # t0
        ("   \n", False),  # t1 (blank) => fine, no corruption log required
        ('{"ts":"x","role":"user","content":"hi"}\n{"role":\n', True),  # t2 invalid JSON => corruption
        ("123\n", True),  # t3 non-dict JSON => corruption
        ('{"ts":"x","role":"system","content":"x"}\n', True),  # t4 invalid role => corruption
    ],
)
def test_us41_symbolic_concolic_paths(tmp_path: Path, caplog, content: str, should_log_corruption: bool) -> None:
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
