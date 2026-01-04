# Test file for User Story 4
# Testing Type: whitebox
# Technique: statement_coverage
# Team Member: sa1068
# Original file: test_user_story_4.py

from vca.core.engine import ChatEngine


def test_engine_returns_fallback_on_dependency_error(monkeypatch) -> None:
    e = ChatEngine()

    def boom(_text: str) -> str:
        raise RuntimeError("forced failure")

    monkeypatch.setattr(e._classifier, "classify", boom)

    out = e.process_turn("hello")
    assert out == "Sorry, something went wrong. Please try again."


def test_engine_continues_after_recoverable_error(monkeypatch) -> None:
    e = ChatEngine()

    calls = {"n": 0}

    def flaky(_text: str) -> str:
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("first call fails")
        return "unknown"

    monkeypatch.setattr(e._classifier, "classify", flaky)

    out1 = e.process_turn("hello")
    out2 = e.process_turn("hello")

    assert out1 == "Sorry, something went wrong. Please try again."
    assert isinstance(out2, str)
    assert out2 != ""
