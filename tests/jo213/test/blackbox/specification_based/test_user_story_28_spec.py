# Test file for User Story 28
# Testing Type: blackbox
# Technique: specification_based
# Team Member: jo213
# Original file: test_user_story_28.py

import json
from pathlib import Path
from vca.storage.history_store import HistoryStore

def test_us28_save_and_load_preserves_timestamps(tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p)

    store.save_turn("hello", "hi")

    turns = store.load_turns(max_turns=10)
    assert len(turns) == 1

    t = turns[0]
    assert t.user_text == "hello"
    assert t.assistant_text == "hi"
    assert t.user_ts is not None
    assert t.assistant_ts is not None

def test_us28_missing_timestamp_is_handled_safely(tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"

    # Older style record without "ts"
    rec1 = {"role": "user", "content": "u1"}
    rec2 = {"role": "assistant", "content": "a1"}

    p.write_text(json.dumps(rec1) + "\n" + json.dumps(rec2) + "\n", encoding="utf-8")

    store = HistoryStore(path=p)
    turns = store.load_turns(max_turns=10)

    assert len(turns) == 1
    assert turns[0].user_text == "u1"
    assert turns[0].assistant_text == "a1"
    assert turns[0].user_ts is None
    assert turns[0].assistant_ts is None
