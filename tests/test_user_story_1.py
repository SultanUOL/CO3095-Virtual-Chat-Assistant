from vca.core.engine import ChatEngine
from vca.core.intents import IntentClassifier
from vca.core.responses import ResponseGenerator


def test_accepts_empty_and_whitespace() -> None:
    c = IntentClassifier()
    assert c.classify("") == "empty"
    assert c.classify("   ") == "empty"


def test_help_and_exit_intents() -> None:
    c = IntentClassifier()
    assert c.classify("help") == "help"
    assert c.classify("HeLp") == "help"
    assert c.classify("exit") == "exit"
    assert c.classify("QUIT") == "exit"


def test_unicode_does_not_crash() -> None:
    c = IntentClassifier()
    assert c.classify("😄") == "unknown"
    assert c.classify("こんにちは") == "unknown"


def test_responses_always_return_string() -> None:
    r = ResponseGenerator()
    assert isinstance(r.generate("empty", ""), str)
    assert isinstance(r.generate("unknown", "hi"), str)
    assert isinstance(r.generate("help", "help"), str)


def test_long_text_is_safe() -> None:
    r = ResponseGenerator()
    long_text = "a" * 100000
    out = r.generate("unknown", long_text)
    assert isinstance(out, str)
    assert len(out) < 1000


def test_engine_returns_response_for_any_input() -> None:
    e = ChatEngine()
    assert isinstance(e.process_turn("hello"), str)
    assert isinstance(e.process_turn(""), str)
    assert isinstance(e.process_turn("   "), str)
    assert isinstance(e.process_turn("✓"), str)


def test_engine_is_deterministic_for_same_input_with_fresh_session() -> None:
    e1 = ChatEngine()
    e2 = ChatEngine()
    assert e1.process_turn("same input") == e2.process_turn("same input")
