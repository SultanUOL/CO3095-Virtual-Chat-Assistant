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


def test_white_box_help_phrase_rule_selected_for_capability_query() -> None:
    c = IntentClassifier()
    result = c.classify_result("what can you do?")

    assert result.intent == Intent.HELP
    assert result.rule == "help_phrase"
    assert result.confidence >= 0.85
    assert all(intent != Intent.QUESTION for intent, _rule in result.candidates)


def test_white_box_priority_still_applies_when_help_and_exit_match() -> None:
    c = IntentClassifier()
    result = c.classify_result("help bye")

    assert result.intent == Intent.EXIT
    assert (Intent.HELP, "help_token") in result.candidates
    assert (Intent.EXIT, "exit_token") in result.candidates


def test_white_box_help_phrase_is_deterministic() -> None:
    c = IntentClassifier()
    r1 = c.classify_result("what can you do")
    r2 = c.classify_result("what can you do")

    assert r1.intent == r2.intent
    assert r1.rule == r2.rule
    assert r1.confidence == r2.confidence