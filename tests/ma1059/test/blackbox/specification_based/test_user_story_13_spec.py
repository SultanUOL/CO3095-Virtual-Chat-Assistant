# Test file for User Story 13
# Testing Type: blackbox
# Technique: specification_based
# Team Member: ma1059
# Original file: test_user_story_13.py

import json
from pathlib import Path
from vca.core.engine import ChatEngine
from vca.storage.interaction_log_store import InteractionLogStore


def test_interaction_log_entry_is_produced(tmp_path: Path) -> None:
    log_path = tmp_path / "interaction_log.jsonl"
    store = InteractionLogStore(path=log_path)

    engine = ChatEngine(interaction_log=store)

    reply = engine.process_turn("hello")
    assert isinstance(reply, str)

    lines = log_path.read_text(encoding="utf8").splitlines()
    assert len(lines) == 1

    event = json.loads(lines[0])
    assert event["input_length"] == len("hello")
    assert event["intent"] == "greeting"
    assert event["fallback_used"] is False
    assert isinstance(event["timestamp_utc"], str)
    assert event["timestamp_utc"].endswith("Z")
