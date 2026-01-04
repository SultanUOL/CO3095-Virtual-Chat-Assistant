# Test file for User Story 37
# Testing Type: blackbox
# Technique: specification_based
# Team Member: wg73
# Original file: test_user_story_37.py

import json
from pathlib import Path
from vca.core.intents import Intent, IntentClassifier


def test_black_box_phrase_dataset_matches_expected_intents() -> None:
    dataset_path = Path(__file__).parent / "us37_phrases.json"
    cases = json.loads(dataset_path.read_text(encoding="utf8"))

    c = IntentClassifier()

    for case in cases:
        text = case["text"]
        expected = Intent(case["expected_intent"])
        assert c.classify(text) == expected, f"{text!r} expected {expected}"
