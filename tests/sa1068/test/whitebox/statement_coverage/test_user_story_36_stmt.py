# Test file for User Story 36
# Testing Type: whitebox
# Technique: statement_coverage
# Team Member: sa1068
# Original file: test_user_story_36.py


from __future__ import annotations
from helpers import FakeHistory, FakeInteractionLog, SeqClock
from vca.core.engine import ChatEngine
from vca.core.intents import Intent


def test_user_story_36_engine_allows_injected_storage_and_clock(monkeypatch) -> None:
    history = FakeHistory()
    log = FakeInteractionLog()
    clock = SeqClock([10.0, 10.123])

    engine = ChatEngine(history=history, interaction_log=log, perf_counter=clock)

    def fixed_intent(_text: str):
        return Intent.HELP

    monkeypatch.setattr(engine, "classify_intent", fixed_intent, raising=True)

    reply = engine.process_turn("help")
    assert isinstance(reply, str)

    assert len(history.saved) == 1
    assert history.saved[0][0] == "help"

    assert len(log.events) == 1
    assert log.events[0]["processing_time_ms"] == 123


def test_user_story_36_engine_uses_safe_fallback_on_processing_error(
    monkeypatch,
) -> None:
    history = FakeHistory()
    log = FakeInteractionLog()
    clock = SeqClock([1.0, 1.01])

    engine = ChatEngine(history=history, interaction_log=log, perf_counter=clock)

    def boom(_text: str, _recent, _context):
        raise RuntimeError("forced")

    monkeypatch.setattr(engine, "route_intent", lambda _intent: boom, raising=True)

    reply = engine.process_turn("hello")
    assert isinstance(reply, str)

    assert len(log.events) == 1
    assert log.events[0]["fallback_used"] is True
