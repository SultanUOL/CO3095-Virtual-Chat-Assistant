# Test file for User Story 38
# Testing Type: blackbox
# Technique: random_based
# Team Member: wg73
# Original file: test_user_story_38.py

from vca.core.intents import Intent, IntentClassifier


def test_synonym_matching_is_case_insensitive_and_trims_whitespace() -> None:
    c = IntentClassifier()
    assert c.classify("  HeY  ") == Intent.GREETING
    assert c.classify("   QUIT") == Intent.EXIT
    assert c.classify("  Commands  ") == Intent.HELP
