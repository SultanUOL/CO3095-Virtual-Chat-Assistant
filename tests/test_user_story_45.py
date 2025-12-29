from __future__ import annotations

from vca.cli.app import CliApp
from vca.cli.commands import Command, parse_user_input


def test_us45_parse_user_input_supports_prefixed_commands_and_unknown() -> None:
    assert parse_user_input("/help").command == Command.HELP
    assert parse_user_input(":commands").command == Command.HELP

    assert parse_user_input("/exit").command == Command.EXIT
    assert parse_user_input(":quit").command == Command.EXIT

    assert parse_user_input("/restart").command == Command.RESTART
    assert parse_user_input(":reset").command == Command.RESTART

    parsed = parse_user_input("/nonsense now")
    assert parsed.command == Command.UNKNOWN
    assert parsed.text == "nonsense"


def test_us45_cli_prints_welcome_and_basic_instructions_on_start() -> None:
    class FakeEngine:
        loaded_turns_count = 0

        def clear_history(self, clear_file: bool = False) -> None:
            return None

        def shutdown(self) -> None:
            return None

    engine = FakeEngine()
    app = CliApp(engine=engine)

    inputs = iter(["exit"])
    outputs: list[str] = []

    def input_fn(_prompt: str) -> str:
        return next(inputs)

    def output_fn(msg: str) -> None:
        outputs.append(msg)

    app.run_with_io(input_fn=input_fn, output_fn=output_fn)

    assert outputs[0] == "Virtual Chat Assistant"
    assert "Type help" in outputs[1]
    assert any("Goodbye" in line for line in outputs)


def test_us45_help_command_prints_available_commands_and_examples_without_engine_call() -> None:
    class FakeEngine:
        loaded_turns_count = 0

        def __init__(self) -> None:
            self.process_calls = 0

        def process_turn(self, _text: str) -> str:
            self.process_calls += 1
            return "should not be called"

        def clear_history(self, clear_file: bool = False) -> None:
            return None

        def shutdown(self) -> None:
            return None

    engine = FakeEngine()
    app = CliApp(engine=engine)

    inputs = iter(["help", "exit"])
    outputs: list[str] = []

    def input_fn(_prompt: str) -> str:
        return next(inputs)

    def output_fn(msg: str) -> None:
        outputs.append(msg)

    app.run_with_io(input_fn=input_fn, output_fn=output_fn)

    joined = "\n".join(outputs)
    assert "Available commands" in joined
    assert "help" in joined
    assert "restart" in joined
    assert "exit" in joined
    assert engine.process_calls == 0


def test_us45_unknown_command_is_friendly_and_suggests_help() -> None:
    class FakeEngine:
        loaded_turns_count = 0

        def __init__(self) -> None:
            self.process_calls = 0

        def process_turn(self, _text: str) -> str:
            self.process_calls += 1
            return "should not be called"

        def clear_history(self, clear_file: bool = False) -> None:
            return None

        def shutdown(self) -> None:
            return None

    engine = FakeEngine()
    app = CliApp(engine=engine)

    inputs = iter(["/doesnotexist", "exit"])
    outputs: list[str] = []

    def input_fn(_prompt: str) -> str:
        return next(inputs)

    def output_fn(msg: str) -> None:
        outputs.append(msg)

    app.run_with_io(input_fn=input_fn, output_fn=output_fn)

    joined = "\n".join(outputs)
    assert "Unknown command" in joined
    assert "Type help" in joined
    assert engine.process_calls == 0
