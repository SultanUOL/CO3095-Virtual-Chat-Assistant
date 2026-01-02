from vca.core.intents import Intent, IntentClassifier
from vca.core.responses import ResponseGenerator


def test_black_box_classifier_supports_multiple_intents() -> None:
    c = IntentClassifier()

    assert c.classify("hello") == Intent.GREETING
    assert c.classify("Hi") == Intent.GREETING

    assert c.classify("help") == Intent.HELP
    assert c.classify("commands") == Intent.HELP

    assert c.classify("What time is it") == Intent.QUESTION
    assert c.classify("Is this working?") == Intent.QUESTION

    assert c.classify("thanks") == Intent.THANKS
    assert c.classify("Thank you") == Intent.THANKS

    assert c.classify("goodbye") == Intent.GOODBYE
    assert c.classify("see you") == Intent.GOODBYE


def test_black_box_classifier_unknown_is_safe_default() -> None:
    c = IntentClassifier()
    assert c.classify("tell me something") == Intent.UNKNOWN
    assert c.classify("random words and an emoji 😀") == Intent.UNKNOWN


def test_black_box_classifier_is_deterministic_for_same_input() -> None:
    c = IntentClassifier()

    samples = [
        "hello",
        "help",
        "What is this",
        "thanks",
        "goodbye",
        "tell me something",
    ]

    for s in samples:
        first = c.classify(s)
        second = c.classify(s)
        assert first == second


def test_white_box_routing_has_handler_path_for_each_intent() -> None:
    r = ResponseGenerator()

    intents = [
        Intent.EMPTY,
        Intent.HELP,
        Intent.HISTORY,
        Intent.EXIT,
        Intent.GREETING,
        Intent.QUESTION,
        Intent.THANKS,
        Intent.GOODBYE,
        Intent.UNKNOWN,
    ]

    for it in intents:
        handler = r.route(it)
        assert callable(handler)

        reply = handler("sample text", None)
        assert isinstance(reply, str)
        assert reply.strip() != ""


def test_white_box_routing_unknown_fallback_for_unrecognised_intent_value() -> None:
    r = ResponseGenerator()
    handler = r.route("not a real intent")
    assert handler("x", None) == r.handle_unknown("x", None)
