"""
CLI layer for the Virtual Chat Assistant.
Handles input and output only.

User story 36 test readiness
The CLI loop is testable using injected input and output functions.

User story 48
Final integration and stability hardening.
"""

from __future__ import annotations

from collections.abc import Callable
import logging
import shutil

from vca.cli.commands import Command, parse_user_input
from vca.cli.help_text import build_help_lines
from vca.core.engine import ChatEngine

logger = logging.getLogger(__name__)

InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]


class CliApp:
    """Console application wrapper."""

    def __init__(self, engine: ChatEngine | None = None) -> None:
        self._engine = engine if engine is not None else ChatEngine()

    @property
    def engine(self) -> ChatEngine:
        return self._engine

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

    def _terminal_width(self) -> int:
        try:
            return int(shutil.get_terminal_size(fallback=(80, 24)).columns)
        except Exception:
            return 80

    def _safe_output(self, output_fn: OutputFn, text: str) -> bool:
        """
        Best effort output. Returns False if output failed.
        If output fails, the application stops because the user
        cannot see responses.
        """
        try:
            output_fn(text)
            return True
        except Exception as ex:
            logger.exception("CLI output error error_type=%s", type(ex).__name__)
            return False

    def run_with_io(
        self,
        input_fn: InputFn,
        output_fn: OutputFn,
        terminal_width: int | None = None,
    ) -> None:
        """Run the CLI loop using injected IO functions for testing."""
        if not self._safe_output(output_fn, "Virtual Chat Assistant"):
            self._safe_shutdown()
            return

        if not self._safe_output(
            output_fn,
            "Type help for commands and examples. Type exit to quit. Type restart to start a new session.",
        ):
            self._safe_shutdown()
            return

        try:
            loaded = getattr(self._engine, "loaded_turns_count", 0)
            if loaded > 0:
                self._safe_output(
                    output_fn, f"(Loaded {loaded} previous turn(s) from history.)"
                )
        except Exception:
            logger.exception("CLI loaded turns message failed")

        width = terminal_width if terminal_width is not None else self._terminal_width()

        try:
            while True:
                try:
                    raw = input_fn("You: ")
                except EOFError:
                    self._safe_shutdown()
                    self._safe_output(output_fn, "Assistant: Goodbye.")
                    break
                except KeyboardInterrupt:
                    raise
                except Exception as ex:
                    logger.exception("CLI input error error_type=%s", type(ex).__name__)
                    self._safe_output(
                        output_fn, "Assistant: Input error. Please try again."
                    )
                    continue

                if raw is None or raw.strip() == "":
                    continue

                try:
                    parsed = parse_user_input(raw)
                except Exception as ex:
                    logger.exception("CLI parse error error_type=%s", type(ex).__name__)
                    self._safe_output(
                        output_fn, "Assistant: Input error. Please try again."
                    )
                    continue

                if parsed.command == Command.EMPTY:
                    continue

                if parsed.command == Command.HELP:
                    try:
                        for line in build_help_lines(width=width):
                            if not self._safe_output(output_fn, line):
                                self._safe_shutdown()
                                return
                    except Exception as ex:
                        logger.exception(
                            "CLI help error error_type=%s", type(ex).__name__
                        )
                        self._safe_output(
                            output_fn, "Assistant: Unable to show help right now."
                        )
                    continue

                if (
                    getattr(Command, "UNKNOWN", None) is not None
                    and parsed.command == Command.UNKNOWN
                ):
                    self._safe_output(
                        output_fn,
                        f"Assistant: Unknown command {parsed.text}. Type help to see commands.",
                    )
                    continue

                if parsed.command == Command.EXIT:
                    try:
                        self._engine.clear_history(clear_file=True)
                    except Exception:
                        pass

                    self._safe_shutdown()
                    self._safe_output(output_fn, "Assistant: Goodbye.")
                    break

                if parsed.command == Command.RESTART:
                    try:
                        self._engine.reset_session()
                        self._safe_output(output_fn, "Assistant: Session restarted.")
                    except Exception as ex:
                        logger.exception(
                            "CLI restart error error_type=%s", type(ex).__name__
                        )
                        self._safe_output(
                            output_fn, "Assistant: Could not restart session."
                        )
                    continue

                try:
                    reply = self._engine.process_turn(parsed.text)
                except Exception as ex:
                    logger.exception(
                        "CLI engine error error_type=%s", type(ex).__name__
                    )
                    self._safe_output(
                        output_fn, "Assistant: Something went wrong. Please try again."
                    )
                    continue

                self._safe_output(output_fn, f"Assistant: {reply}")

        except KeyboardInterrupt:
            self._safe_shutdown()
            self._safe_output(output_fn, "")
            self._safe_output(output_fn, "Assistant: Goodbye.")


def run_cli(
    engine: ChatEngine,
    *,
    input_fn: InputFn,
    output_fn: OutputFn,
    terminal_width: int | None = None,
) -> None:
    """
    Compatibility entry point for tests that import run_cli from this module.
    """
    CliApp(engine=engine).run_with_io(
        input_fn=input_fn,
        output_fn=output_fn,
        terminal_width=terminal_width,
    )
