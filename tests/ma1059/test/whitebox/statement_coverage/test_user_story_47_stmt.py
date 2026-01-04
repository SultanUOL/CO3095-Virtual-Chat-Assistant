# Test file for User Story 47
# Testing Type: whitebox
# Technique: statement_coverage
# Team Member: ma1059
# Original file: test_user_story_47.py

from __future__ import annotations
import json
from pathlib import Path
from vca.core.engine import ChatEngine
from vca.domain.chat_turn import ChatTurn
from vca.storage.history_store import HistoryStore


def _write_jsonl_turns(path: Path, turns: list[ChatTurn]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for t in turns:
            f.write(
                json.dumps(
                    {"ts": "20250101T000000Z", "role": "user", "content": t.user_text},
                    ensure_ascii=False,
                )
                + "\n"
            )
            f.write(
                json.dumps(
                    {
                        "ts": "20250101T000000Z",
                        "role": "assistant",
                        "content": t.assistant_text,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )


def test_user_story_47_startup_and_restart_reliability(tmp_path: Path) -> None:
    """
    Combined testing for User Story 47 in a single test.

    Black box testing
    Treat engine as a unit, verify observable behaviour of restart and state.

    White box testing
    Assert internal state properties that prove deterministic behaviour and no duplication.

    Symbolic testing
    Define path conditions and invariants, then test representative inputs for each condition.

    Concolic testing
    Run concrete inputs that cover different branches and validate the same invariants.
    """

    history_path = tmp_path / "history.jsonl"
    turns = [
        ChatTurn(user_text="hello", assistant_text="hi"),
        ChatTurn(user_text="help", assistant_text="here is help"),
        ChatTurn(user_text="bye", assistant_text="goodbye"),
    ]
    _write_jsonl_turns(history_path, turns)

    history = HistoryStore(path=history_path, max_turns=500)

    # Black box testing
    engine = ChatEngine(history=history)
    assert engine.loaded_turns_count == 3
    assert len(engine.session.turns) == 3

    before_file_lines = history_path.read_text(encoding="utf-8").splitlines()
    assert len(before_file_lines) == 6

    # White box testing
    before_session_id = engine.session.session_id
    before_messages_len = len(engine.session.messages)
    before_turns_len = len(engine.session.turns)
    assert before_turns_len == 3
    assert before_messages_len >= 6

    engine.reset_session()

    after_session_id = engine.session.session_id
    after_messages_len = len(engine.session.messages)
    after_turns_len = len(engine.session.turns)

    assert after_session_id != before_session_id
    assert after_turns_len == 3
    assert after_messages_len >= 6

    # No file duplication
    after_file_lines = history_path.read_text(encoding="utf-8").splitlines()
    assert after_file_lines == before_file_lines

    # Determinism across repeated restarts
    engine.reset_session()
    assert len(engine.session.turns) == 3
    assert history_path.read_text(encoding="utf-8").splitlines() == before_file_lines

    # Symbolic testing
    # Path condition A empty history
    empty_path = tmp_path / "empty.jsonl"
    empty_history = HistoryStore(path=empty_path, max_turns=500)
    empty_engine = ChatEngine(history=empty_history)
    assert len(empty_engine.session.turns) == 0
    empty_engine.reset_session()
    assert len(empty_engine.session.turns) == 0
