# Test file for User Story 34
# Testing Type: whitebox
# Technique: path_coverage
# Team Member: sa1068
# Original file: test_user_story_34.py

from __future__ import annotations
from pathlib import Path
from vca.cli.app import CliApp
from vca.core.engine import ChatEngine
from vca.storage.history_store import HistoryStore

def test_user_story_34_engine_returns_safe_fallback_on_unhandled_exception(
    monkeypatch,
) -> None:
    engine = ChatEngine()
    engine._responder.fallback_error = lambda: "fallback"  # type: ignore[assignment]

    def boom(_raw):
        raise RuntimeError("boom")

    monkeypatch.setattr(engine, "_stage_validate", boom)

    out = engine.process_turn("hello")
    assert out == "fallback"
