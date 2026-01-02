from __future__ import annotations

from pathlib import Path

from vca.core.engine import ChatEngine
from vca.core.intents import IntentClassifier
from vca.core.logging_config import configure_logging
from vca.storage.history_store import HistoryStore
from vca.storage.interaction_log_store import InteractionLogStore


def test_us31_forced_exception_is_logged_with_context_and_user_sees_friendly_fallback(
    tmp_path: Path, monkeypatch
) -> None:
    log_path = tmp_path / "system_errors.log"
    configure_logging(log_file_path=log_path, force=True)

    history = HistoryStore(path=tmp_path / "history.jsonl")
    interaction = InteractionLogStore(path=tmp_path / "interaction_log.jsonl")
    engine = ChatEngine(history=history, interaction_log=interaction)

    def boom(self, _text: str):
        raise ZeroDivisionError("forced")

    monkeypatch.setattr(IntentClassifier, "classify", boom)

    out = engine.process_turn("hello")
    assert out == "Sorry, something went wrong. Please try again."

    text = log_path.read_text(encoding="utf-8")
    assert "error_type=ZeroDivisionError" in text
    assert "intent=Intent.UNKNOWN" in text
    assert "file_operation=False" in text
