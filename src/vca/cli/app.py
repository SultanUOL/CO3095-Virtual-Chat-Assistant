"""
CLI layer for the Virtual Chat Assistant.
Handles input and output only.
"""

from __future__ import annotations

from collections.abc import Callable

from vca.cli.commands import Command, parse_user_input
from vca.core.engine import ChatEngine


InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]


class CliApp:
    """Console application wrapper."""

    def __init__(self, engine: ChatEngine | None = None) -> None:
        self._engine = engine if engine is not None else ChatEngine()

    def run(self) -> None:
        """Run using real console IO."""
        self.run_with_io(input_fn=input, output_fn=print)

    def run_with_io(self, input_fn: InputFn, output_fn: OutputFn) -> None:
        """Run the CLI loop using injected IO functions for testing."""
        output_fn("Virtual Chat Assistant")
        output_fn("Type help for commands. Type exit to quit.")
        if self._engine.loaded_turns_count > 0:
            output_fn(f"(Loaded {self._engine.loaded_turns_count} previous turn(s) from history.)")

        try:
            while True:
                try:
                    raw = input_fn("You: ")
                except EOFError:
                    output_fn("Assistant: Goodbye.")
                    break

                parsed = parse_user_input(raw)

                if parsed.command == Command.EXIT:
                    self._engine.clear_history(clear_file=True)
                    output_fn("Assistant: Goodbye.")
                    break

                reply = self._engine.process_turn(parsed.text)
                output_fn(f"Assistant: {reply}")

        except KeyboardInterrupt:
            output_fn("")
            output_fn("Assistant: Goodbye.")