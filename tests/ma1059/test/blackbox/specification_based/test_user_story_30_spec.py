# Test file for User Story 30
# Testing Type: blackbox
# Technique: specification_based
# Team Member: ma1059
# Original file: test_user_story_30.py

from __future__ import annotations
import json
from pathlib import Path
from vca.core.intents import Intent
from vca.core.engine import ChatEngine
from vca.storage.history_store import HistoryStore
from vca.storage.interaction_log_store import InteractionLogStore


def test_us30_engine_writes_interaction_event_after_turn(tmp_path: Path) -> None:
    history_path = tmp_path / "history.jsonl"
    interaction_path = tmp_path / "interaction_log.jsonl"

    history = HistoryStore(path=history_path)
    interaction_log = InteractionLogStore(path=interaction_path)
    engine = ChatEngine(history=history, interaction_log=interaction_log)

    _ = engine.process_turn("hi")

    lines = interaction_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1

    event = json.loads(lines[0])
    assert {
        "timestamp_utc",
        "input_length",
        "intent",
        "confidence",
        "fallback_used",
        "processing_time_ms",
    }.issubset(event.keys())

    assert event["input_length"] == 2
    assert event["processing_time_ms"] >= 0
    assert "content" not in event


def test_us30_interaction_log_store_clamps_and_writes_event(tmp_path: Path) -> None:
    log_path = tmp_path / "interaction_log.jsonl"
    store = InteractionLogStore(path=log_path)

    store.append_event(
        input_length=-5,
        intent=Intent.GREETING,
        fallback_used=False,
        confidence=2.5,
        processing_time_ms=-10,
    )

    lines = log_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1

    obj = json.loads(lines[0])
    assert obj["input_length"] == 0
    assert obj["intent"] == "greeting"
    assert obj["confidence"] == 1.0
    assert obj["fallback_used"] is False
    assert obj["processing_time_ms"] == 0
    assert "timestamp_utc" in obj
