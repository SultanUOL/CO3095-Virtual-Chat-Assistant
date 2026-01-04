# Test file for User Story 5
# Testing Type: blackbox
# Technique: random_based
# Team Member: wg73
# Original file: test_user_story_5.py

from vca.core.intents import Intent, IntentClassifier


def test_classifier_detects_help() -> None:
    c = IntentClassifier()
    assert c.classify("help") == Intent.HELP
    assert c.classify("?") == Intent.HELP


def test_classifier_detects_greeting() -> None:
    c = IntentClassifier()
    assert c.classify("hello") == Intent.GREETING
    assert c.classify("Hi") == Intent.GREETING
    assert c.classify("good morning") == Intent.GREETING


def test_classifier_detects_question() -> None:
    c = IntentClassifier()
    assert c.classify("What time is it") == Intent.QUESTION
    assert c.classify("how are you") == Intent.QUESTION
    assert c.classify("Is this working") == Intent.QUESTION
    assert c.classify("Is this working?") == Intent.QUESTION


def test_classifier_unknown_is_explicit() -> None:
    c = IntentClassifier()
    assert c.classify("tell me something") == Intent.UNKNOWN


def test_classifier_is_deterministic_for_same_input() -> None:
    c = IntentClassifier()
    first = c.classify("hello")
    second = c.classify("hello")
    assert first == second
    assert first == Intent.GREETING
