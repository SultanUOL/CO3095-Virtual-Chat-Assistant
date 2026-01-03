# Test file for User Story 44
# Testing Type: blackbox
# Technique: specification_based
# Team Member: jo213
# Original file: test_user_story_44.py

from pathlib import Path
from vca.storage.history_store import HistoryStore

def test_us44_storage_bounded_applies_history_limit(tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, max_turns=50)

    for i in range(200):
        store.save_turn(f"u{i}", f"a{i}")

    turns = store.load_turns(max_turns=9999)
    assert len(turns) == 50
    assert turns[0].user_text == "u150"
    assert turns[-1].user_text == "u199"

def test_us44_corruption_handling_safe_on_startup(tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"
    p.write_text('{"role":"user","content":"hi"}\n{not json}\n', encoding="utf-8")

    store = HistoryStore(path=p, max_turns=10)

    turns = store.load_turns()
    assert turns == []
