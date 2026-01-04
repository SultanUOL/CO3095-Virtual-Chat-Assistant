# Test file for User Story 38
# Testing Type: whitebox
# Technique: branch_coverage
# Team Member: wg73
# Original file: test_user_story_38.py

from vca.core.intents import Intent, IntentClassifier


def test_synonym_rules_do_not_override_higher_priority_exit() -> None:
    c = IntentClassifier()
    result = c.classify_result("bye exit")

    assert result.intent == Intent.EXIT
    assert any(i == Intent.EXIT for i, _r in result.candidates)
