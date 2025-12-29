from __future__ import annotations

from vca.cli.app import CliApp
from vca.cli.help_text import build_help_lines


def test_us46_help_command_produces_commands_and_two_examples() -> None:
    class FakeEngine:
        loaded_turns_count = 0

        def __init__(self) -> None:
            self.process_calls = 0

        def process_turn(self, _text: str) -> str:
            self.process_calls += 1
            return "should not be called"

        def clear_history(self, clear_file: bool = False) -> None:
            return None

        def reset_session(self) -> None:
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

    app.run_with_io(input_fn=input_fn, output_fn=output_fn, terminal_width=80)

    joined = "\n".join(outputs)
    assert "Available commands" in joined
    assert "Example interactions" in joined
    assert "You: help" in joined
    assert "You: restart" in joined
    assert engine.process_calls == 0


def test_us46_help_text_is_wrapped_to_terminal_width() -> None:
    width = 60
    lines = build_help_lines(width=width)
    assert len(lines) > 0
    assert all(len(line) <= width for line in lines)
