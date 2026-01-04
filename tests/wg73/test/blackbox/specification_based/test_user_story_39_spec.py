# Test file for User Story 39
# Testing Type: blackbox
# Technique: specification_based
# Team Member: wg73
# Original file: test_user_story_39.py

import json
from pathlib import Path
from vca.core.engine import ChatEngine
from vca.core.intents import Intent, IntentClassifier
from vca.storage.interaction_log_store import InteractionLogStore


def test_black_box_false_positive_regression_set() -> None:
    dataset_path = Path(__file__).parent / "us39_false_positives.json"
    cases = json.loads(dataset_path.read_text(encoding="utf8"))

    c = IntentClassifier()

    for case in cases:
        text = case["text"]
        expected = Intent(case["expected_intent"])
        assert c.classify(text) == expected, f"{text!r} expected {expected}"


def test_logs_record_when_multiple_rules_matched(tmp_path: Path) -> None:
    log_path = tmp_path / "interaction_log.jsonl"
    store = InteractionLogStore(path=log_path)
    engine = ChatEngine(interaction_log=store)

    engine.process_turn("help bye")

    event = json.loads(log_path.read_text(encoding="utf8").splitlines()[0])
    assert event["rule_match_count"] >= 2
    assert event["multiple_rules_matched"] is True
