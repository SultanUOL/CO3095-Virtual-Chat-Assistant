import json
from pathlib import Path

from vca.core.intents import Intent, IntentClassifier


def test_black_box_false_positive_regression_set() -> None:
    dataset_path = Path(__file__).parent / "us39_false_positives.json"
    cases = json.loads(dataset_path.read_text(encoding="utf8"))

    c = IntentClassifier()

    for case in cases:
        text = case["text"]
        expected = Intent(case["expected_intent"])
        assert c.classify(text) == expected, f"{text!r} expected {expected}"