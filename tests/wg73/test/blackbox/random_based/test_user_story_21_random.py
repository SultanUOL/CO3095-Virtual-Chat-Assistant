# Test file for User Story 21
# Testing Type: blackbox
# Technique: random_based
# Team Member: wg73
# Original file: test_user_story_21.py

from vca.core.intents import Intent, IntentClassifier


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
