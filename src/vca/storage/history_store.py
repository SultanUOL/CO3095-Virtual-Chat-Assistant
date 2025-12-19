"""
File based storage for chat history.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import List, Union


class HistoryStore:
    """Stores and loads chat history from disk."""

    DEFAULT_PATH = Path("data") / "history.txt"

    def __init__(self, path: Union[str, Path, None] = None) -> None:
        # Predictable default path, but allow override for tests.
        self._path = Path(path) if path is not None else self.DEFAULT_PATH

    @property
    def path(self) -> Path:
        return self._path

    def save_turn(self, user_text: str, assistant_text: str) -> None:
        """Append one conversation turn to the history file.

        Format is line-based so it is easy to inspect and test.
        Newlines are escaped to keep each field on one line.
        """
        self._path.parent.mkdir(parents=True, exist_ok=True)

        ts = _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

        user = self._escape_newlines(user_text)
        assistant = self._escape_newlines(assistant_text)

        block = (
            f"[{ts}] USER: {user}\n"
            f"[{ts}] ASSISTANT: {assistant}\n"
            "---\n"
        )

        with self._path.open("a", encoding="utf-8") as f:
            f.write(block)

    def load_history(self) -> List[str]:
        """Load prior history lines .

        If the file does not exist, returns an empty list.
        """
        if not self._path.exists():
            return []
        with self._path.open("r", encoding="utf-8") as f:
            return [line.rstrip("\n") for line in f.readlines()]

    @staticmethod
    def _escape_newlines(text: str) -> str:
        return ("" if text is None else str(text)).replace("\r\n", "\\n").replace("\n", "\\n")
