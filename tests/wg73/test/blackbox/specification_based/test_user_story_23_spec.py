# Test file for User Story 23
# Testing Type: blackbox
# Technique: specification_based
# Team Member: wg73
# Original file: test_user_story_23.py

import json
from pathlib import Path
from vca.core.engine import ChatEngine, CONFIDENCE_THRESHOLD
from vca.storage.interaction_log_store import InteractionLogStore


def test_low_confidence_triggers_clarification_question_and_logs_confidence(
    tmp_path: Path,
) -> None:
    log_path = tmp_path / "interaction_log.jsonl"
    store = InteractionLogStore(path=log_path)

    engine = ChatEngine(interaction_log=store)

    out1 = engine.process_turn("help bye")
    assert isinstance(out1, str)
    assert "Reply 1" in out1
    assert "Reply 2" in out1

    event = json.loads(log_path.read_text(encoding="utf8").splitlines()[0])
    assert 0.0 <= event["confidence"] <= 1.0
    assert event["confidence"] < CONFIDENCE_THRESHOLD
