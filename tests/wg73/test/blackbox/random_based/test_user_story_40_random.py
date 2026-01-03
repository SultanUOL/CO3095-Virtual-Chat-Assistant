# Test file for User Story 40
# Testing Type: blackbox
# Technique: random_based
# Team Member: wg73
# Original file: test_user_story_40.py

from __future__ import annotations
from vca.core.engine import ChatEngine
from vca.core.intents import Intent, IntentClassifier
from vca.core.responses import ResponseGenerator

def test_us40_engine_routes_each_supported_intent_without_error_fallback() -> None:
    gen = ResponseGenerator()
    error_text = gen.fallback_error()

    samples = [
        "",
        "help",
        "commands",
        "exit",
        "quit",
        "history",
        "show history",
        "hello",
        "hi",
        "what is python",
        "why is the sky blue",
        "thanks",
        "cheers",
        "goodbye",
        "see you",
        "asdasdasd",
        "qwertyuiop",
    ]

    for text in samples:
        e = ChatEngine()
        out = e.process_turn(text)
        assert isinstance(out, str)
        assert out != error_text
