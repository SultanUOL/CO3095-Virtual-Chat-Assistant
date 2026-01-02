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


def test_white_box_partial_matches_do_not_create_wrong_candidates() -> None:
    c = IntentClassifier()

    r1 = c.classify_result("this")
    assert all(intent != Intent.GREETING for intent, _rule in r1.candidates)

    r2 = c.classify_result("show helpful tips")
    assert all(intent != Intent.HELP for intent, _rule in r2.candidates)

    r3 = c.classify_result("prehistory")
    assert all(intent != Intent.HISTORY for intent, _rule in r3.candidates)

    r4 = c.classify_result("quitely")
    assert all(intent != Intent.EXIT for intent, _rule in r4.candidates)


def test_white_box_exact_command_rules_are_preferred_for_help_and_exit() -> None:
    c = IntentClassifier()

    help_result = c.classify_result("help")
    assert help_result.intent == Intent.HELP
    assert help_result.rule == "help_exact"
    assert help_result.confidence >= 0.90

    exit_result = c.classify_result("exit")
    assert exit_result.intent == Intent.EXIT
    assert exit_result.rule == "exit_exact"
    assert exit_result.confidence >= 0.90


def test_logs_record_when_multiple_rules_matched(tmp_path: Path) -> None:
    log_path = tmp_path / "interaction_log.jsonl"
    store = InteractionLogStore(path=log_path)
    engine = ChatEngine(interaction_log=store)

    engine.process_turn("help bye")

    event = json.loads(log_path.read_text(encoding="utf8").splitlines()[0])
    assert event["rule_match_count"] >= 2
    assert event["multiple_rules_matched"] is True
