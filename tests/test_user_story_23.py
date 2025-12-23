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


def test_low_confidence_triggers_ambiguous_path(tmp_path: Path) -> None:
    log_path = tmp_path / "interaction_log.jsonl"
    store = InteractionLogStore(path=log_path)

    engine = ChatEngine(interaction_log=store)

    out = engine.process_turn("help bye")
    assert out == "I am not fully sure what you meant. Please rephrase, or type help to see commands."

    event = json.loads(log_path.read_text(encoding="utf8").splitlines()[0])
    assert 0.0 <= event["confidence"] <= 1.0
    assert event["confidence"] < CONFIDENCE_THRESHOLD


def test_high_confidence_does_not_trigger_ambiguous() -> None:
    engine = ChatEngine()
    out = engine.process_turn("help")
    assert isinstance(out, str)
    assert "Commands" in out