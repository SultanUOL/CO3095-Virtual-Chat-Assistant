"""vca.cli.commands

Pure command parsing for the CLI layer.

This module contains no IO so it can be unit tested easily.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Command(str, Enum):
    EMPTY = "empty"
    HELP = "help"
    EXIT = "exit"
    RESTART = "restart"
    MESSAGE = "message"
    UNKNOWN = "unknown"


_HELP_TOKENS = {"help", "h", "?", "commands"}
_EXIT_TOKENS = {"exit", "quit", "q", "bye"}
_RESTART_TOKENS = {"restart", "reset", "startover", "start over"}


@dataclass(frozen=True)
class ParsedInput:
    command: Command
    text: str


def parse_user_input(raw_text: object) -> ParsedInput:
    """Parse raw user input into a command and a cleaned text payload."""
    text = "" if raw_text is None else str(raw_text)
    stripped = text.strip()
    lower = stripped.casefold()

    # Support optional command prefixes such as /help or :exit.
    prefix = ""
    if stripped[:1] in {"/", ":"}:
        prefix = stripped[1:].strip()

    if stripped == "":
        return ParsedInput(command=Command.EMPTY, text="")

    if lower in _HELP_TOKENS:
        return ParsedInput(command=Command.HELP, text="help")

    if lower in _EXIT_TOKENS:
        return ParsedInput(command=Command.EXIT, text="exit")

    if lower in _RESTART_TOKENS:
        return ParsedInput(command=Command.RESTART, text="restart")

    if prefix != "":
        lower_prefix = prefix.casefold()

        if lower_prefix in _HELP_TOKENS:
            return ParsedInput(command=Command.HELP, text="help")

        if lower_prefix in _EXIT_TOKENS:
            return ParsedInput(command=Command.EXIT, text="exit")

        if lower_prefix in _RESTART_TOKENS:
            return ParsedInput(command=Command.RESTART, text="restart")

        name = prefix.split()[0] if prefix.split() else prefix
        return ParsedInput(command=Command.UNKNOWN, text=name)

    return ParsedInput(command=Command.MESSAGE, text=text)
