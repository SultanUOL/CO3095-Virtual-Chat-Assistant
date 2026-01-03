# Test file for User Story 44
# Testing Type: whitebox
# Technique: statement_coverage
# Team Member: jo213
# Original file: test_user_story_44.py

from pathlib import Path
from vca.storage.history_store import HistoryStore

def test_us44_default_load_is_bounded_and_uses_last_lines(
    tmp_path: Path, monkeypatch
) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, max_turns=30)

    for i in range(120):
        store.save_turn(f"u{i}", f"a{i}")

    calls = {"all": 0, "last": 0}

    def _all():
        calls["all"] += 1
        return []

    def _last(max_lines: int):
        calls["last"] += 1
        # naive implementation for the test, but enough to prove bounded path is used
        lines = []
        with p.open("r", encoding="utf-8") as f:
            for ln in f:
                lines.append(ln.rstrip("\n"))
        return lines[-max_lines:]

    monkeypatch.setattr(store, "_stream_all_lines", _all)
    monkeypatch.setattr(store, "_stream_last_lines", _last)

    turns = store.load_turns()  # max_turns None -> bounded default path
    assert len(turns) <= 30
    assert calls["last"] >= 1
    assert calls["all"] == 0
