from __future__ import annotations

import argparse
import logging
import sys
from typing import Iterable

from vca.core.engine import ChatEngine

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """
    CLI argument parser.

    Keeps parsing isolated so invalid args can be handled safely in main.
    """
    parser = argparse.ArgumentParser(prog="vca", description="Virtual Chat Assistant")
    parser.add_argument(
        "--no-exit-on-goodbye",
        action="store_true",
        help="Keep running even if the assistant replies with goodbye",
    )
    return parser


def _safe_input(prompt: str) -> str | None:
    """
    Safe wrapper around input().

    Returns None for EOF and raises KeyboardInterrupt for caller handling.
    Any other error is logged and treated as a recoverable input failure.
    """
    try:
        return input(prompt)
    except KeyboardInterrupt:
        raise
    except EOFError:
        return None
    except Exception as ex:
        logger.exception("CLI input error error_type=%s", type(ex).__name__)
        return ""


def _safe_print(lines: Iterable[str]) -> None:
    """
    Safe wrapper around printing.

    If console output fails, we still exit cleanly.
    """
    try:
        for line in lines:
            print(line)
    except Exception:
        pass


def run_cli(engine: ChatEngine, *, exit_on_goodbye: bool = True) -> int:
    """
    Main interactive loop.

    Acceptance criteria
    Handles invalid input and interruptions safely and returns an exit code.
    """
    _safe_print(["Virtual Chat Assistant. Type 'exit' to quit."])

    while True:
        try:
            raw = _safe_input("> ")
            if raw is None:
                _safe_print(["", "End of input. Exiting."])
                return 0

            user_text = raw

        except KeyboardInterrupt:
            _safe_print(["", "Interrupted. Exiting."])
            return 0

        if user_text.strip().casefold() in {"exit", "quit", "q"}:
            _safe_print(["Goodbye"])
            return 0

        try:
            reply = engine.process_turn(user_text)
        except Exception as ex:
            logger.exception("CLI processing error error_type=%s", type(ex).__name__)
            _safe_print(["Something went wrong. Please try again."])
            continue

        _safe_print([reply])

        if exit_on_goodbye and reply.strip().casefold() == "goodbye":
            return 0


def main(argv: list[str] | None = None) -> int:
    """
    Program entry point.

    Parses args safely and runs the CLI loop with defensive shutdown.
    """
    if argv is None:
        argv = sys.argv[1:]

    try:
        parser = build_parser()
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    except Exception as ex:
        logger.exception("CLI argument parse failed error_type=%s", type(ex).__name__)
        _safe_print(["Invalid arguments."])
        return 2

    try:
        engine = ChatEngine()
    except Exception as ex:
        logger.exception("Engine init failed error_type=%s", type(ex).__name__)
        _safe_print(["Failed to start."])
        return 1

    try:
        return run_cli(engine, exit_on_goodbye=not args.no_exit_on_goodbye)
    finally:
        try:
            engine.shutdown()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
