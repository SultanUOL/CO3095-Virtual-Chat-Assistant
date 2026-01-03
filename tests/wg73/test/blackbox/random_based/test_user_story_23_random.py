# Test file for User Story 23
# Testing Type: blackbox
# Technique: random_based
# Team Member: wg73
# Original file: test_user_story_23.py

import json
from pathlib import Path
from vca.core.engine import ChatEngine, CONFIDENCE_THRESHOLD
from vca.core.intents import IntentClassifier
from vca.storage.interaction_log_store import InteractionLogStore

def test_high_confidence_does_not_trigger_clarification() -> None:
    engine = ChatEngine()
    out = engine.process_turn("help")
    assert isinstance(out, str)
    assert "Commands" in out
    assert "Did you mean" not in out
