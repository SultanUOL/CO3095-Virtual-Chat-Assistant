from __future__ import annotations

from typing import List

from vca.cli.app import CliApp
from vca.cli.commands import Command, parse_user_input


class _FakeEngine:
    def __init__(self) -> None:
        self.loaded_turns_count = 0
        self.cleared = False
        self.seen: List[str] = []

    def process_turn(self, text: str) -> str:
        self.seen.append(text)
        return f"reply:{text}"

    def clear_history(self, clear_file: bool = True) -> None:
        self.cleared = True


def test_parse_user_input_commands() -> None:
    assert parse_user_input("").command == Command.EMPTY
    assert parse_user_input("   ").command == Command.EMPTY
    assert parse_user_input("help").command == Command.HELP
    assert parse_user_input("EXIT").command == Command.EXIT
    assert parse_user_input("hello").command == Command.MESSAGE


def test_cli_loop_prompts_until_exit_and_prints_responses() -> None:
    engine = _FakeEngine()
    app = CliApp(engine=engine)

    inputs = iter(["", "help", "hello", "exit"])
    outputs: List[str] = []

    def input_fn(_prompt: str) -> str:
        return next(inputs)

    def output_fn(text: str) -> None:
        outputs.append(text)

    app.run_with_io(input_fn=input_fn, output_fn=output_fn)

    assert engine.cleared is True
    assert engine.seen == ["hello"]
    assert any(o.startswith("Assistant: reply:") for o in outputs)
    assert outputs[-1] == "Assistant: Goodbye."


def test_cli_handles_eof_as_exit() -> None:
    engine = _FakeEngine()
    app = CliApp(engine=engine)

    outputs: List[str] = []

    def input_fn(_prompt: str) -> str:
        raise EOFError

    def output_fn(text: str) -> None:
        outputs.append(text)

    app.run_with_io(input_fn=input_fn, output_fn=output_fn)

    assert outputs[-1] == "Assistant: Goodbye."
