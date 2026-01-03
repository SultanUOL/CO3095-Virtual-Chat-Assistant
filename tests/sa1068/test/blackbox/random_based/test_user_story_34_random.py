# Test file for User Story 34
# Testing Type: blackbox
# Technique: random_based
# Team Member: sa1068
# Original file: test_user_story_34.py

from __future__ import annotations
from pathlib import Path
from vca.cli.app import CliApp
from vca.core.engine import ChatEngine
from vca.storage.history_store import HistoryStore

def test_user_story_34_cli_handles_keyboard_interrupt() -> None:
    engine = ChatEngine()
    app = CliApp(engine=engine)

    def input_fn(_prompt: str) -> str:
        raise KeyboardInterrupt

    outputs: list[str] = []

    def output_fn(s: str) -> None:
        outputs.append(s)

    app.run_with_io(input_fn=input_fn, output_fn=output_fn, terminal_width=80)

    combined = "\n".join(outputs).lower()
    assert "goodbye" in combined

def test_user_story_34_cli_handles_eof() -> None:
    engine = ChatEngine()
    app = CliApp(engine=engine)

    def input_fn(_prompt: str) -> str:
        raise EOFError

    outputs: list[str] = []

    def output_fn(s: str) -> None:
        outputs.append(s)

    app.run_with_io(input_fn=input_fn, output_fn=output_fn, terminal_width=80)

    combined = "\n".join(outputs).lower()
    assert "goodbye" in combined

def test_user_story_34_cli_recovers_from_input_error() -> None:
    engine = ChatEngine()
    app = CliApp(engine=engine)

    calls = {"n": 0}

    def input_fn(_prompt: str) -> str:
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("weird input failure")
        return "exit"

    outputs: list[str] = []

    def output_fn(s: str) -> None:
        outputs.append(s)

    app.run_with_io(input_fn=input_fn, output_fn=output_fn, terminal_width=80)

    combined = "\n".join(outputs).lower()
    assert "input error" in combined or "goodbye" in combined
