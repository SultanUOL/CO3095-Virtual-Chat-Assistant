# Test file for User Story 3
# Testing Type: blackbox
# Technique: random_based
# Team Member: sa1068
# Original file: test_user_story_3.py

from vca.core.engine import ChatEngine
from vca.core.validator import InputValidator

def test_validator_trims_whitespace() -> None:
    v = InputValidator()
    out = v.clean("   hello   ")
    assert out.text == "hello"
    assert out.was_truncated is False

def test_validator_empty_is_safe() -> None:
    v = InputValidator()
    out = v.clean("   ")
    assert out.text == ""

def test_validator_removes_control_characters() -> None:
    v = InputValidator()
    out = v.clean("hi\x00\x01there")
    assert out.text == "hithere"

def test_validator_truncates_long_input() -> None:
    v = InputValidator()
    long_text = "a" * (v.MAX_LEN + 10)
    out = v.clean(long_text)
    assert len(out.text) == v.MAX_LEN
    assert out.was_truncated is True

def test_engine_handles_long_input_without_crash_and_warns() -> None:
    e = ChatEngine()
    v = InputValidator()
    long_text = "b" * (v.MAX_LEN + 50)
    reply = e.process_turn(long_text)
    assert "truncated" in reply.lower()

def test_engine_handles_unusual_characters_without_crash() -> None:
    e = ChatEngine()
    reply = e.process_turn("hello ✓ 😄 こんにちは")
    assert isinstance(reply, str)
