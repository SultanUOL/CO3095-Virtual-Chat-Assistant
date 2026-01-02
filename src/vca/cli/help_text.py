"""vca.cli.help_text

Help and usage text for the CLI.

The goal is to keep help content in one place and ensure it is readable in a
normal terminal width by wrapping long lines.
"""

from __future__ import annotations

import textwrap


def _wrap_prefixed(prefix: str, text: str, width: int) -> list[str]:
    width = max(30, int(width))
    content_width = max(10, width - len(prefix))

    chunks = textwrap.wrap(
        text,
        width=content_width,
        break_long_words=False,
        break_on_hyphens=False,
    )

    if not chunks:
        return [prefix.rstrip()]

    lines: list[str] = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            lines.append(f"{prefix}{chunk}")
        else:
            lines.append(f"{' ' * len(prefix)}{chunk}")
    return lines


def build_help_lines(width: int = 80) -> list[str]:
    """Return help output lines, wrapped to the given width."""
    width = max(30, int(width))

    lines: list[str] = []

    lines.extend(_wrap_prefixed("Assistant: ", "Available commands", width))
    lines.extend(
        _wrap_prefixed("Assistant: ", "help     Show commands and examples", width)
    )
    lines.extend(
        _wrap_prefixed("Assistant: ", "restart  Start a new in memory session", width)
    )
    lines.extend(_wrap_prefixed("Assistant: ", "exit     Quit the application", width))
    lines.append("Assistant:")

    lines.extend(_wrap_prefixed("Assistant: ", "Example interactions", width))
    lines.extend(_wrap_prefixed("You: ", "help", width))
    lines.extend(
        _wrap_prefixed("Assistant: ", "Shows the command list and examples", width)
    )
    lines.append("Assistant:")
    lines.extend(_wrap_prefixed("You: ", "restart", width))
    lines.extend(_wrap_prefixed("Assistant: ", "Session restarted.", width))
    lines.append("Assistant:")
    lines.extend(_wrap_prefixed("You: ", "exit", width))
    lines.extend(_wrap_prefixed("Assistant: ", "Goodbye.", width))

    return lines
