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

    def _safe_shutdown(self) -> None:
        """Best effort shutdown hook. Never raises."""
        shutdown = getattr(self._engine, "shutdown", None)
        if callable(shutdown):
            try:
                shutdown()
            except Exception:
                pass

    def run_with_io(self, input_fn: InputFn, output_fn: OutputFn) -> None:
        """Run the CLI loop using injected IO functions for testing."""
        output_fn("Virtual Chat Assistant")
        output_fn("Type help for commands. Type exit to quit. Type restart to start a new session.")
        if getattr(self._engine, "loaded_turns_count", 0) > 0:
            output_fn(f"(Loaded {self._engine.loaded_turns_count} previous turn(s) from history.)")

        try:
            while True:
                try:
                    raw = input_fn("You: ")
                except EOFError:
                    # Treat end of input as a clean shutdown.
                    self._safe_shutdown()
                    output_fn("Assistant: Goodbye.")
                    break

                parsed = parse_user_input(raw)

                if parsed.command == Command.EXIT:
                    # Keep prior behavior for existing tests: exit clears persisted history.
                    try:
                        self._engine.clear_history(clear_file=True)
                    except Exception:
                        pass

                    # US32 addition: flush and finalise any pending work without crashing.
                    self._safe_shutdown()

                    output_fn("Assistant: Goodbye.")
                    break

                if parsed.command == Command.RESTART:
                    # Restart only resets in memory session state.
                    try:
                        self._engine.reset_session()
                    except Exception:
                        pass
                    output_fn("Assistant: Session restarted.")
                    continue

                reply = self._engine.process_turn(parsed.text)
                output_fn(f"Assistant: {reply}")

        except KeyboardInterrupt:
            # Ctrl C should be clean and user friendly, no traceback.
            self._safe_shutdown()
            output_fn("")
            output_fn("Assistant: Goodbye.")