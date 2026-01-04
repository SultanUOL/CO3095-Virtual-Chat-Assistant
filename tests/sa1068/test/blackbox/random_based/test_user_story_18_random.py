# Test file for User Story 18
# Testing Type: blackbox
# Technique: random_based
# Team Member: sa1068
# Original file: test_user_story_18.py

from vca.core.engine import ChatEngine


def test_followup_question_references_previous_topic() -> None:
    engine = ChatEngine()

    engine.process_turn("I am visiting Leicester tomorrow")
    response = engine.process_turn("Where is the station?")

    assert "leicester" in response.lower()


def test_pronoun_followup_references_previous_topic() -> None:
    engine = ChatEngine()

    engine.process_turn("Tell me about train tickets")
    response = engine.process_turn("How much does it cost?")

    assert "train" in response.lower()


def test_missing_previous_message_falls_back_cleanly() -> None:
    engine = ChatEngine()

    response = engine.process_turn("How much does it cost?")

    assert response
    assert "following up on your earlier message" not in response.lower()
