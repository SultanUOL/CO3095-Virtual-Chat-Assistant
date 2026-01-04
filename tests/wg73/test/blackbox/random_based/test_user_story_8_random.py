# Test file for User Story 8
# Testing Type: blackbox
# Technique: random_based
# Team Member: wg73
# Original file: test_user_story_8.py

from vca.core.responses import ResponseGenerator


def test_unknown_intent_returns_fixed_response_for_multiple_inputs() -> None:
    r = ResponseGenerator()
    expected = "I did not understand that. Please rephrase your message or type help."

    assert r.generate("unknown", "tell me something", recent_messages=[]) == expected
    assert r.generate("unknown", "😀", recent_messages=[]) == expected
    assert r.generate("unknown", "%%%###@@@", recent_messages=[]) == expected


def test_unknown_intent_does_not_crash_on_empty_input() -> None:
    r = ResponseGenerator()
    expected = "I did not understand that. Please rephrase your message or type help."

    assert r.generate("unknown", "", recent_messages=[]) == expected
