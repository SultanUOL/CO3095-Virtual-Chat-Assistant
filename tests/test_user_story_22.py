from vca.core.intents import Intent, IntentClassifier


def test_priority_exit_beats_help_when_both_match() -> None:
    c = IntentClassifier()
    out = c.classify("help bye")
    assert out == Intent.EXIT
    assert c.last_decision is not None
    assert c.last_decision.intent == Intent.EXIT


def test_priority_help_beats_greeting_when_both_match() -> None:
    c = IntentClassifier()
    out = c.classify("hello help")
    assert out == Intent.HELP
    assert c.last_decision is not None
    assert c.last_decision.intent == Intent.HELP


def test_priority_greeting_beats_question_when_both_match() -> None:
    c = IntentClassifier()
    out = c.classify("hello?")
    assert out == Intent.GREETING
    assert c.last_decision is not None
    assert c.last_decision.intent == Intent.GREETING


def test_priority_help_beats_question_when_both_match() -> None:
    c = IntentClassifier()
    out = c.classify("help?")
    assert out == Intent.HELP
    assert c.last_decision is not None
    assert c.last_decision.intent == Intent.HELP
