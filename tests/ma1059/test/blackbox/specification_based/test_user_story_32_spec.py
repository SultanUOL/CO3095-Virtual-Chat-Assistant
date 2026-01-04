# Test file for User Story 32
# Testing Type: blackbox
# Technique: specification_based
# Team Member: ma1059
# Original file: test_user_story_32.py

from __future__ import annotations
from pathlib import Path
from vca.core.engine import ChatEngine
from vca.storage.history_store import HistoryStore
from vca.storage.interaction_log_store import InteractionLogStore


def test_us32_engine_shutdown_is_safe_and_history_is_not_corrupted(
    tmp_path: Path,
) -> None:
    history_path = tmp_path / "history.jsonl"
    interaction_path = tmp_path / "interaction_log.jsonl"

    engine = ChatEngine(
        history=HistoryStore(path=history_path),
        interaction_log=InteractionLogStore(path=interaction_path),
    )

    _ = engine.process_turn("hi")
    engine.shutdown()

    text = history_path.read_text(encoding="utf-8").strip()
    assert text != ""
    for line in text.splitlines():
        assert line.startswith("{") and line.endswith("}")
