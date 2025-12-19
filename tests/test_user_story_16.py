from __future__ import annotations

from typing import List

from vca.cli.app import CliApp
from vca.cli.commands import Command, parse_user_input


class _FakeEngine:
    def __init__(self) -> None:
        self.loaded_turns_count = 0
        self.cleared = False
        self.reset_calls = 0
        self.seen: List[str] = []

    def process_turn(self, text: str) -> str:
        self.seen.append(text)
        return f"reply:{text}"

    def clear_history(self, clear_file: bool = True) -> None:
        self.cleared = True

    def reset_session(self) -> None:
        self.reset_calls += 1
        self.seen.clear()


def test_parse_restart_command() -> None:
    assert parse_user_input("restart").command == Command.RESTART
    assert parse_user_input("RESET").command == Command.RESTART


def test_cli_restart_resets_session_and_continues() -> None:
    engine = _FakeEngine()
    app = CliApp(engine=engine)

    inputs = iter(["hello", "restart", "hello again", "exit"])
    outputs: List[str] = []

    def input_fn(_prompt: str) -> str:
        return next(inputs)

    def output_fn(text: str) -> None:
        outputs.append(text)

    app.run_with_io(input_fn=input_fn, output_fn=output_fn)

    assert engine.reset_calls == 1
    assert engine.cleared is True
    assert "Assistant: Session restarted." in outputs
    assert engine.seen == ["hello again"]
    assert outputs[-1] == "Assistant: Goodbye."
