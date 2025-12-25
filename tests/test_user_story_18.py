from vca.core.engine import ChatEngine

def test_debug_loaded_responses_module_path() -> None:
    import inspect
    import vca.core.responses as responses

    print("responses.py loaded from:", responses.__file__)
    src = inspect.getsource(responses.ResponseGenerator.extract_topic_from_last_user_message)
    assert "about\\s+" in src


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
    assert "earlier message" not in response.lower()
