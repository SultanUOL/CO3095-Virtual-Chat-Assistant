# Test file for User Story 40
# Testing Type: whitebox
# Technique: statement_coverage
# Team Member: wg73
# Original file: test_user_story_40.py

from __future__ import annotations
from vca.core.intents import Intent
from vca.core.responses import ResponseGenerator


def test_us40_supported_intents_have_handlers() -> None:
    gen = ResponseGenerator()

    samples = [
        (Intent.EMPTY, ""),
        (Intent.HELP, "help"),
        (Intent.HELP, "commands"),
        (Intent.EXIT, "exit"),
        (Intent.EXIT, "quit"),
        (Intent.HISTORY, "history"),
        (Intent.HISTORY, "show history"),
        (Intent.GREETING, "hello"),
        (Intent.GREETING, "hi"),
        (Intent.QUESTION, "what is python"),
        (Intent.QUESTION, "why is the sky blue"),
        (Intent.THANKS, "thanks"),
        (Intent.THANKS, "cheers"),
        (Intent.GOODBYE, "goodbye"),
        (Intent.GOODBYE, "see you"),
        (Intent.UNKNOWN, "asdasdasd"),
        (Intent.UNKNOWN, "qwertyuiop"),
    ]

    for intent, text in samples:
        handler = gen.route(intent)
        assert callable(handler)

        out = handler(text, [], [])
        assert isinstance(out, str)

        if intent == Intent.UNKNOWN:
            assert out == gen.fallback_unknown()
        else:
            assert out != gen.fallback_unknown()
