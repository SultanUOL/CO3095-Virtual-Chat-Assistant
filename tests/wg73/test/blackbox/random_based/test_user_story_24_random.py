# Test file for User Story 24
# Testing Type: blackbox
# Technique: random_based
# Team Member: wg73
# Original file: test_user_story_24.py

from vca.core.engine import ChatEngine

def test_ambiguous_flow_asks_then_resolves() -> None:
    e = ChatEngine()

    first = e.process_turn("help bye")
    assert "Did you mean" in first
    assert "Reply 1" in first
    assert "Reply 2" in first

    second = e.process_turn("2")
    assert "Commands" in second

def test_ambiguous_flow_falls_back_if_user_does_not_clarify() -> None:
    e = ChatEngine()

    first = e.process_turn("help bye")
    assert "Did you mean" in first

    second = e.process_turn("maybe")
    assert "type help" in second.casefold()

    third = e.process_turn("help")
    assert "Commands" in third
