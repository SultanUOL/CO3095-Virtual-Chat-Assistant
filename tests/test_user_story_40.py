# tests/test_user_story_40.py
from __future__ import annotations

from vca.core.engine import ChatEngine
from vca.core.intents import Intent, IntentClassifier
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


def test_us40_priority_is_still_enforced_in_classifier() -> None:
    c = IntentClassifier()

    r1 = c.classify_result("exit help")
    r2 = c.classify_result("help exit")

    assert r1.intent == Intent.EXIT
    assert r2.intent == Intent.EXIT
