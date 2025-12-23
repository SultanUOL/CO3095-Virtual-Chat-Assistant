# src/vca/storage/history_store.py
from __future__ import annotations

import json
from collections import deque
from pathlib import Path
from typing import Union

from vca.domain.chat_turn import ChatTurn
from vca.domain.constants import HISTORY_MAX_TURNS


class HistoryStore:
    """
    File backed history store using JSONL.

    Each conversation turn is stored as two JSON lines:
    one user record, then one assistant record.

    Trimming keeps the most recent N turns (2N lines).
    """

    DEFAULT_PATH = Path("data") / "history.jsonl"

    def __init__(
        self,
        path: Union[str, Path, None] = None,
        *,
        max_turns: int = HISTORY_MAX_TURNS,
    ) -> None:
        # Path can be overridden for tests or alternative deployments
        self._path = Path(path) if path is not None else self.DEFAULT_PATH

        # Defensive: ensure max_turns is a positive integer
        coerced = int(max_turns)
        self._max_turns = coerced if coerced > 0 else int(HISTORY_MAX_TURNS)

    @property
    def path(self) -> Path:
        """Expose the resolved history file path for diagnostics and tests."""
        return self._path

    @property
    def max_turns(self) -> int:
        """Expose the configured maximum number of turns retained on disk."""
        return self._max_turns

    def save_turn(self, user_text: str, assistant_text: str) -> None:
        """
        Append one conversation turn to the JSONL file, then trim to max_turns.

        We store empty strings for None inputs to keep the on disk schema stable.
        """
        self._path.parent.mkdir(parents=True, exist_ok=True)

        records = [
            {"role": "user", "content": "" if user_text is None else str(user_text)},
            {"role": "assistant", "content": "" if assistant_text is None else str(assistant_text)},
        ]

        with self._path.open("a", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        # Enforce retention after every write so the file never grows unbounded
        self._trim_file_to_last_n_turns(self._max_turns)

    def load_turns(self, max_turns: int | None = None) -> list[ChatTurn]:
        """
        Load up to max_turns most recent conversation turns.

        If max_turns is None, uses the store configured max_turns.
        Returns an empty list if the file does not exist.
        """
        if not self._path.exists():
            return []

        effective = self._max_turns if max_turns is None else int(max_turns)
        lines = self._stream_last_lines(max_lines=effective * 2) if effective and effective > 0 else []

        records: list[tuple[str, str]] = []
        for line in lines:
            if not line.strip():
                continue

            obj = json.loads(line)
            role = str(obj.get("role", "")).strip().lower()
            content = "" if obj.get("content") is None else str(obj.get("content", ""))

            records.append((role, content))

        # Reconstruct turns from alternating user and assistant records
        turns: list[ChatTurn] = []
        pending_user: str | None = None

        for role, content in records:
            if role == "user":
                pending_user = content
            elif role == "assistant" and pending_user is not None:
                turns.append(ChatTurn(user_text=pending_user, assistant_text=content))
                pending_user = None

        return turns

    def _stream_last_lines(self, max_lines: int) -> list[str]:
        """
        Stream the last max_lines from the file efficiently.

        This avoids loading the entire file into memory when max_turns is small.
        """
        buf: deque[str] = deque(maxlen=max_lines)
        with self._path.open("r", encoding="utf-8") as f:
            for line in f:
                buf.append(line.rstrip("\n"))
        return list(buf)

    def _trim_file_to_last_n_turns(self, max_turns: int) -> None:
        """
        Keep only the last max_turns turns on disk.

        Since each turn is stored as two lines, we keep at most 2 * max_turns lines.
        """
        if not self._path.exists():
            return

        lines = self._path.read_text(encoding="utf-8").splitlines()
        keep = lines[-(max_turns * 2) :] if max_turns > 0 else []

        # Preserve trailing newline when there is content, helps text tools and diffs
        self._path.write_text("\n".join(keep) + ("\n" if keep else ""), encoding="utf-8")
