# Test file for User Story 23
# Testing Type: whitebox
# Technique: branch_coverage
# Team Member: wg73
# Original file: test_user_story_23.py

import json
from pathlib import Path
from vca.core.engine import ChatEngine, CONFIDENCE_THRESHOLD
from vca.core.intents import IntentClassifier
from vca.storage.interaction_log_store import InteractionLogStore

def test_confidence_is_between_zero_and_one_and_deterministic() -> None:
    c = IntentClassifier()

    r1 = c.classify_result("help")
    r2 = c.classify_result("help")

    assert 0.0 <= r1.confidence <= 1.0
    assert r1.intent == r2.intent
    assert r1.confidence == r2.confidence
    assert r1.confidence >= 0.9
