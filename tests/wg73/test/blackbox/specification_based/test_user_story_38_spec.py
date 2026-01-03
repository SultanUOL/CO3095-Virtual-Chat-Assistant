# Test file for User Story 38
# Testing Type: blackbox
# Technique: specification_based
# Team Member: wg73
# Original file: test_user_story_38.py

import json
from pathlib import Path
from vca.core.engine import ChatEngine
from vca.core.intents import Intent, IntentClassifier
from vca.storage.interaction_log_store import InteractionLogStore

def test_black_box_synonym_dataset_matches_expected_intents() -> None:
    dataset_path = Path(__file__).parent / "us38_synonyms.json"
    cases = json.loads(dataset_path.read_text(encoding="utf8"))

    c = IntentClassifier()

    for case in cases:
        text = case["text"]
        expected = Intent(case["expected_intent"])
        assert c.classify(text) == expected, f"{text!r} expected {expected}"

def test_logs_show_chosen_intent_for_synonym_match(tmp_path: Path) -> None:
    log_path = tmp_path / "interaction_log.jsonl"
    store = InteractionLogStore(path=log_path)
    engine = ChatEngine(interaction_log=store)

    engine.process_turn("  HeY  ")

    first_line = log_path.read_text(encoding="utf8").splitlines()[0]
    event = json.loads(first_line)
    assert event["intent"] == "greeting"
