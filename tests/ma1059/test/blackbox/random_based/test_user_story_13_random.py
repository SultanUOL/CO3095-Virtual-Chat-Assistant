# Test file for User Story 13
# Testing Type: blackbox
# Technique: random_based
# Team Member: ma1059
# Original file: test_user_story_13.py

import json
from pathlib import Path
from vca.core.engine import ChatEngine
from vca.storage.interaction_log_store import InteractionLogStore

def test_logging_failure_does_not_crash(tmp_path: Path) -> None:
    bad_path = tmp_path / "logdir"
    bad_path.mkdir(parents=True, exist_ok=True)

    store = InteractionLogStore(path=bad_path)
    engine = ChatEngine(interaction_log=store)

    reply = engine.process_turn("hello")
    assert isinstance(reply, str)
