from vca.core.engine import ChatEngine
from vca.core.intents import IntentClassifier
from vca.core.responses import ResponseGenerator


def test_us20_unknown_intent_fallback_suggests_next_action() -> None:
    e = ChatEngine()
    out = e.process_turn("asdasdasd qqqq zzzz")
    lowered = out.lower()
    assert "help" in lowered or "rephrase" in lowered


def test_us20_error_fallback_is_different_from_unknown_and_has_no_exception_details(
    monkeypatch,
) -> None:
    e = ChatEngine()

    def boom(_text: str):
        raise RuntimeError("forced failure details")

    monkeypatch.setattr(IntentClassifier, "classify", boom)

    error_out = e.process_turn("hello")

    rg = ResponseGenerator()
    unknown_out = rg.fallback_unknown()

    assert error_out != unknown_out
    assert "forced" not in error_out.lower()
    assert "runtimeerror" not in error_out.lower()
