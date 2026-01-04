# Test file for User Story 12
# Testing Type: blackbox
# Technique: random_based
# Team Member: jo213
# Original file: test_user_story_12.py

from pathlib import Path
from vca.core.engine import ChatEngine
from vca.storage.history_store import HistoryStore


def test_clear_history_clears_memory_and_file(tmp_path: Path) -> None:
    p = tmp_path / "history.txt"
    engine = ChatEngine(history=HistoryStore(path=p))

    engine.process_turn("hello")
    assert len(engine.session.messages) > 0
    assert p.exists()

    engine.clear_history(clear_file=True)
    assert len(engine.session.messages) == 0
    assert not p.exists()
