from vca.core.engine import ChatEngine


def test_each_intent_maps_to_specific_handler() -> None:
    e = ChatEngine()

    assert e.route_intent("empty").__name__ == "handle_empty"
    assert e.route_intent("help").__name__ == "handle_help"
    assert e.route_intent("history").__name__ == "handle_history"
    assert e.route_intent("exit").__name__ == "handle_exit"

    assert e.route_intent("greeting").__name__ == "handle_greeting"
    assert e.route_intent("question").__name__ == "handle_question"


def test_unknown_intent_routes_to_default_handler() -> None:
    e = ChatEngine()
    assert e.route_intent("something new").__name__ == "handle_unknown"
    assert e.route_intent(None).__name__ == "handle_unknown"


def test_routing_is_testable_without_cli() -> None:
    e = ChatEngine()

    help_handler = e.route_intent("help")
    out = help_handler("help", [])
    assert "Commands:" in out

    unknown_handler = e.route_intent("unknown")
    out2 = unknown_handler("hello", [])
    assert "type help" in out2


def test_router_chooses_correct_handler_for_known_inputs() -> None:
    e = ChatEngine()

    intent = e.classify_intent("help")
    assert e.route_intent(intent).__name__ == "handle_help"

    intent2 = e.classify_intent("exit")
    assert e.route_intent(intent2).__name__ == "handle_exit"
