# Test file for User Story 40
# Testing Type: whitebox
# Technique: branch_coverage
# Team Member: wg73
# Original file: test_user_story_40.py

from __future__ import annotations
from vca.core.intents import Intent, IntentClassifier


def test_us40_priority_is_still_enforced_in_classifier() -> None:
    c = IntentClassifier()

    r1 = c.classify_result("exit help")
    r2 = c.classify_result("help exit")

    assert r1.intent == Intent.EXIT
    assert r2.intent == Intent.EXIT
