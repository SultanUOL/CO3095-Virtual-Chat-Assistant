"""
File based storage for chat history.
"""

from __future__ import annotations
from vca.domain.chat_turn import ChatTurn

import datetime as _dt
from pathlib import Path
from typing import List, Union
from vca.domain.constants import HISTORY_MAX_TURNS


class HistoryStore:
    """Stores and loads chat history from disk."""

    DEFAULT_PATH = Path("data") / "history.txt"

    def __init__(self, path: Union[str, Path, None] = None) -> None:
        # Predictable default path, but allow override for tests.
        self._path = Path(path) if path is not None else self.DEFAULT_PATH

    @property
    def path(self) -> Path:
        return self._path

    def clear_file(self) -> None:
        """Delete history file if it exists (non-fatal)."""
        try:
            if self._path.exists():
                self._path.unlink()
        except Exception:
            return

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

        self._trim_file_to_last_n_turns(HISTORY_MAX_TURNS)

    def load_turns(self) -> list[ChatTurn]:
        if not self._path.exists():
            return []

        turns = []
        user = None
        assistant = None

        for line in self.load_history():
            if line.startswith("USER: "):
                user = line.replace("USER: ", "")
            elif line.startswith("ASSISTANT: "):
                assistant = line.replace("ASSISTANT: ", "")
            elif " USER: " in line:
                user = line.split(" USER: ", 1)[1]
            elif " ASSISTANT: " in line:
                assistant = line.split(" ASSISTANT: ", 1)[1]

            elif line.strip() == "---":
                if user is not None and assistant is not None:
                    turns.append(ChatTurn(user, assistant))
                user = None
                assistant = None

        return turns

    def _trim_file_to_last_n_turns(self, max_turns: int) -> None:
        try:
            if not self._path.exists():
                return

            text = self._path.read_text(encoding="utf-8")
            if not text.strip():
                return

            blocks = text.split("---\n")
            blocks = [b for b in blocks if b.strip()]
            blocks = blocks[-max_turns:]

            new_text = ""
            for b in blocks:
                new_text += b.rstrip("\n") + "\n---\n"

            self._path.write_text(new_text, encoding="utf-8")
        except Exception:
            # trimming must never crash app
            return

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
