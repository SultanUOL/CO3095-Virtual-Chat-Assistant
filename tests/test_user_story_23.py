import json
from pathlib import Path

from vca.core.engine import ChatEngine, CONFIDENCE_THRESHOLD
from vca.core.intents import IntentClassifier
from vca.storage.interaction_log_store import InteractionLogStore


def test_confidence_is_between_zero_and_one_and_deterministic() -> None:
    c = IntentClassifier()

    r1 = c.classify_result("help")
    r2 = c.classify_result("help")

    assert 0.0 <= r1.confidence <= 1.0
    assert r1.intent == r2.intent
    assert r1.confidence == r2.confidence
    assert r1.confidence >= 0.9


def test_low_confidence_triggers_clarification_question_and_logs_confidence(tmp_path: Path) -> None:
    log_path = tmp_path / "interaction_log.jsonl"
    store = InteractionLogStore(path=log_path)

    engine = ChatEngine(interaction_log=store)

    out1 = engine.process_turn("help bye")
    assert isinstance(out1, str)
    assert "Reply 1" in out1
    assert "Reply 2" in out1

    event = json.loads(log_path.read_text(encoding="utf8").splitlines()[0])
    assert 0.0 <= event["confidence"] <= 1.0
    assert event["confidence"] < CONFIDENCE_THRESHOLD


def test_clarification_choice_resolves_and_clears_pending_state() -> None:
    engine = ChatEngine()

    out1 = engine.process_turn("help bye")
    assert "Reply 1" in out1
    assert "Reply 2" in out1

    out2 = engine.process_turn("1")
    assert isinstance(out2, str)
    assert "Reply 1" not in out2
    assert "Reply 2" not in out2

    out3 = engine.process_turn("help")
    assert isinstance(out3, str)
    assert "Commands" in out3


def test_high_confidence_does_not_trigger_clarification() -> None:
    engine = ChatEngine()
    out = engine.process_turn("help")
    assert isinstance(out, str)
    assert "Commands" in out
