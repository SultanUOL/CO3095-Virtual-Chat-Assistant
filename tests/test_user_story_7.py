from vca.core.responses import ResponseGenerator


def test_faq_help() -> None:
    r = ResponseGenerator()
    assert r.faq_response_for("help") == "Commands: help, history, exit. You can also type a message to get a basic reply."
    assert r.faq_response_for("  HELP  ") == "Commands: help, history, exit. You can also type a message to get a basic reply."


def test_faq_what_can_you_do() -> None:
    r = ResponseGenerator()
    assert r.faq_response_for("what can you do") == "I can respond to greetings and questions, show session history, and explain commands. Type help."
    assert r.faq_response_for("  What can you do?  ") == "I can respond to greetings and questions, show session history, and explain commands. Type help."


def test_faq_who_are_you() -> None:
    r = ResponseGenerator()
    assert r.faq_response_for("who are you") == "I am a virtual chat assistant built for coursework as a simple deterministic CLI assistant."
    assert r.faq_response_for("  WHO ARE YOU  ") == "I am a virtual chat assistant built for coursework as a simple deterministic CLI assistant."


def test_faq_how_do_i_exit() -> None:
    r = ResponseGenerator()
    assert r.faq_response_for("how do i exit") == "Type exit or quit to close the assistant."
    assert r.faq_response_for(" How do I exit? ") == "Type exit or quit to close the assistant."


def test_faq_how_is_history_stored() -> None:
    r = ResponseGenerator()
    assert r.faq_response_for("how is history stored") == "History is stored in a text file at data/history.txt (appended after each turn)."
    assert r.faq_response_for("HOW IS HISTORY STORED ") == "History is stored in a text file at data/history.txt (appended after each turn)."


def test_non_matching_prompt_returns_none_and_uses_normal_flow() -> None:
    r = ResponseGenerator()

    assert r.faq_response_for("tell me a joke") is None

    out = r.generate("unknown", "tell me a joke", recent_messages=[])
    assert "type help" in out

