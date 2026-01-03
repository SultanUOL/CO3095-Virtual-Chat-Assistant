# Test file for User Story 17
# Testing Type: blackbox
# Technique: random_based
# Team Member: sa1068
# Original file: test_user_story_17.py

from vca.core.engine import ChatEngine
from vca.core.intents import Intent
from vca.core.responses import ResponseGenerator
from vca.domain.chat_turn import ChatTurn
from vca.domain.constants import CONTEXT_WINDOW_TURNS

def test_context_window_constant_is_defined() -> None:
    assert isinstance(CONTEXT_WINDOW_TURNS, int)
    assert CONTEXT_WINDOW_TURNS == 3

def test_response_differs_with_and_without_context() -> None:
    engine = ChatEngine()

    response_no_context = engine.process_turn("Where is the station?")

    engine.reset_session()

    engine.process_turn("I am visiting Leicester tomorrow")
    response_with_context = engine.process_turn("Where is the station?")

    assert response_no_context != response_with_context
    assert "Following up on your earlier message" in response_with_context

def test_context_is_deterministic_for_same_history_and_input() -> None:
    r = ResponseGenerator()
    context = [
        ChatTurn(user_text="I am visiting Leicester tomorrow", assistant_text="Okay"),
        ChatTurn(user_text="I need travel advice", assistant_text="Sure"),
    ]

    a = r.generate(Intent.QUESTION, "Where is the station?", None, context)
    b = r.generate(Intent.QUESTION, "Where is the station?", None, context)

    assert a == b
