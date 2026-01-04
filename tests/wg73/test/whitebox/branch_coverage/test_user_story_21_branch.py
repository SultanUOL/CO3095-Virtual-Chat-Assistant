# Test file for User Story 21
# Testing Type: whitebox
# Technique: branch_coverage
# Team Member: wg73
# Original file: test_user_story_21.py

from vca.core.intents import Intent
from vca.core.responses import ResponseGenerator


def test_white_box_routing_has_handler_path_for_each_intent() -> None:
    r = ResponseGenerator()

    intents = [
        Intent.EMPTY,
        Intent.HELP,
        Intent.HISTORY,
        Intent.EXIT,
        Intent.GREETING,
        Intent.QUESTION,
        Intent.THANKS,
        Intent.GOODBYE,
        Intent.UNKNOWN,
    ]

    for it in intents:
        handler = r.route(it)
        assert callable(handler)

        reply = handler("sample text", None)
        assert isinstance(reply, str)
        assert reply.strip() != ""


def test_white_box_routing_unknown_fallback_for_unrecognised_intent_value() -> None:
    r = ResponseGenerator()
    handler = r.route("not a real intent")
    assert handler("x", None) == r.handle_unknown("x", None)
