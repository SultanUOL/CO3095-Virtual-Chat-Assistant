# Test file for User Story 20
# Testing Type: blackbox
# Technique: random_based
# Team Member: sa1068
# Original file: test_user_story_20.py

from vca.core.engine import ChatEngine


def test_us20_unknown_intent_fallback_suggests_next_action() -> None:
    e = ChatEngine()
    out = e.process_turn("asdasdasd qqqq zzzz")
    lowered = out.lower()
    assert "help" in lowered or "rephrase" in lowered
