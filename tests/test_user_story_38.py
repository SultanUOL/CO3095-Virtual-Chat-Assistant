import json
from pathlib import Path

from vca.core.intents import Intent, IntentClassifier


def test_black_box_synonym_dataset_matches_expected_intents() -> None:
    dataset_path = Path(__file__).parent / "us38_synonyms.json"
    cases = json.loads(dataset_path.read_text(encoding="utf8"))

    c = IntentClassifier()

    for case in cases:
        text = case["text"]
        expected = Intent(case["expected_intent"])
        assert c.classify(text) == expected, f"{text!r} expected {expected}"