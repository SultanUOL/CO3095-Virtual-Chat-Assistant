# Test file for User Story 27
# Testing Type: blackbox
# Technique: specification_based
# Team Member: jo213
# Original file: test_user_story_27.py

from pathlib import Path
from vca.storage.history_store import HistoryStore


def test_us27_missing_history_file_starts_empty(tmp_path: Path) -> None:
    store = HistoryStore(path=tmp_path / "missing.jsonl")
    assert store.load_turns() == []


def test_us27_corrupted_history_file_returns_empty_and_logs(
    tmp_path: Path, caplog
) -> None:
    p = tmp_path / "history.jsonl"
    p.write_text(
        '{"ts":"x","role":"user","content":"hi"}\nNOT JSON\n', encoding="utf-8"
    )

    store = HistoryStore(path=p)

    with caplog.at_level("ERROR"):
        turns = store.load_turns()

    assert turns == []
    assert any("History file is corrupted" in rec.message for rec in caplog.records)
