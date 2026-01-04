# Test file for User Story 2
# Testing Type: blackbox
# Technique: random_based
# Team Member: sa1068
# Original file: test_user_story_2.py

from vca.core.engine import ChatEngine
from vca.domain.session import ConversationSession


def test_new_session_starts_when_engine_starts() -> None:
    e = ChatEngine()
    assert isinstance(e.session, ConversationSession)
    assert e.session.session_id is not None
    assert len(e.session.messages) == 0


def test_each_turn_is_recorded_in_order() -> None:
    e = ChatEngine()
    r1 = e.process_turn("hello")
    r2 = e.process_turn("how are you")

    msgs = list(e.session.messages)
    assert msgs[0].role == "user"
    assert msgs[0].content == "hello"
    assert msgs[1].role == "assistant"
    assert msgs[1].content == r1
    assert msgs[2].role == "user"
    assert msgs[2].content == "how are you"
    assert msgs[3].role == "assistant"
    assert msgs[3].content == r2


def test_engine_can_access_recent_messages_for_generation() -> None:
    e = ChatEngine()
    e.process_turn("hello")
    out = e.process_turn("hello")
    assert "Messages this session" in out


def test_new_run_starts_new_session_by_default() -> None:
    e1 = ChatEngine()
    e2 = ChatEngine()
    assert e1.session.session_id != e2.session.session_id


def test_session_history_growth_stays_stable() -> None:
    e = ChatEngine()
    for i in range(500):
        e.process_turn(f"msg {i}")
    assert len(e.session.messages) == 1000
