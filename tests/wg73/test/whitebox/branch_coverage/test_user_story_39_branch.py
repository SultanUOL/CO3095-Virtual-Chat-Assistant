# Test file for User Story 39
# Testing Type: whitebox
# Technique: branch_coverage
# Team Member: wg73
# Original file: test_user_story_39.py

from vca.core.intents import Intent, IntentClassifier


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
