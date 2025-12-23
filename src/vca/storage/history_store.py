"""
File based storage for chat history."""

from __future__ import annotations

import datetime as _dt
import json
import logging
from collections import deque
from pathlib import Path
from typing import Union

from vca.domain.chat_turn import ChatTurn
from vca.domain.constants import HISTORY_MAX_TURNS

logger = logging.getLogger(__name__)


class HistoryStore:
    """Stores and loads chat history from disk."""

    DEFAULT_PATH = Path("data") / "history.jsonl"

    def __init__(self, path: Union[str, Path, None] = None) -> None:
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
        """Append one conversation turn to the history file."""
        self._path.parent.mkdir(parents=True, exist_ok=True)

        # Legacy storage
        if self._path.suffix.lower() == ".txt":
            self._save_turn_legacy(user_text, assistant_text)
            self._trim_file_to_last_n_turns(HISTORY_MAX_TURNS)
            return

        # JSONL storage (US25)
        ts = self._utc_iso()
        records = [
            {"ts": ts, "role": "user", "content": "" if user_text is None else str(user_text)},
            {"ts": ts, "role": "assistant", "content": "" if assistant_text is None else str(assistant_text)},
        ]

        with self._path.open("a", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        self._trim_file_to_last_n_turns(HISTORY_MAX_TURNS)

    def load_turns(self, max_turns: int | None = HISTORY_MAX_TURNS) -> list[ChatTurn]:
        """
        Load persisted conversation turns safely and efficiently."""
        if not self._path.exists():
            return []

        # Legacy load (safe)
        if self._path.suffix.lower() == ".txt":
            try:
                return self._load_turns_legacy()
            except Exception as ex:
                logger.error("History file is corrupted (legacy format). Starting with empty history.", exc_info=ex)
                return []

        # JSONL load (streaming)
        try:
            if max_turns is None or max_turns <= 0:
                lines = self._stream_all_lines()
            else:
                lines = self._stream_last_lines(max_lines=max_turns * 2)
        except Exception as ex:
            logger.error("Failed to read history file. Starting with empty history.", exc_info=ex)
            return []

        records: list[tuple[str, str]] = []
        corruption_detected = False

        for line in lines:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as ex:
                corruption_detected = True
                logger.error("History file is corrupted (invalid JSON). Starting with empty history.", exc_info=ex)
                break

            if not isinstance(obj, dict):
                corruption_detected = True
                logger.error("History file is corrupted (non-object JSON). Starting with empty history.")
                break

            role = str(obj.get("role", "")).strip().lower()
            if role not in ("user", "assistant"):
                corruption_detected = True
                logger.error("History file is corrupted (invalid role). Starting with empty history.")
                break

            content = obj.get("content", "")
            records.append((role, "" if content is None else str(content)))

        if corruption_detected:
            return []

        # Reconstruct turns (pairs)
        turns: list[ChatTurn] = []
        pending_user: str | None = None

        for role, content in records:
            if role == "user":
                pending_user = content
            elif role == "assistant":
                if pending_user is not None:
                    turns.append(ChatTurn(pending_user, content))
                    pending_user = None

        return turns

    def load_history(self) -> list[str]:

        if not self._path.exists():
            return []
        with self._path.open("r", encoding="utf-8") as f:
            return [line.rstrip("\n") for line in f.readlines()]

    # -------------------------
    # Streaming helpers (US26)
    # -------------------------

    def _stream_all_lines(self) -> list[str]:
        lines: list[str] = []
        with self._path.open("r", encoding="utf-8") as f:
            for line in f:
                lines.append(line.rstrip("\n"))
        return lines

    def _stream_last_lines(self, max_lines: int) -> list[str]:
        """Efficiently stream only the last max_lines from file."""
        buf = deque(maxlen=max_lines)
        with self._path.open("r", encoding="utf-8") as f:
            for line in f:
                buf.append(line.rstrip("\n"))
        return list(buf)

    # -------------------------
    # Internal helpers
    # -------------------------

    @staticmethod
    def _utc_iso() -> str:
        return _dt.datetime.now(tz=_dt.timezone.utc).replace(microsecond=0).isoformat()

    def _trim_file_to_last_n_turns(self, max_turns: int) -> None:
        """Keep only the most recent N turns in the file."""
        if not self._path.exists():
            return

        if self._path.suffix.lower() == ".txt":
            lines = self.load_history()
            blocks: list[list[str]] = []
            current: list[str] = []
            for line in lines:
                current.append(line)
                if line.strip() == "---":
                    blocks.append(current)
                    current = []
            if current:
                blocks.append(current)

            keep = blocks[-max_turns:] if max_turns > 0 else []
            flat = [ln for block in keep for ln in block]
            with self._path.open("w", encoding="utf-8") as f:
                for ln in flat:
                    f.write(ln + "\n")
            return

        lines = self.load_history()
        keep_lines = lines[-(max_turns * 2) :] if max_turns > 0 else []
        with self._path.open("w", encoding="utf-8") as f:
            for ln in keep_lines:
                f.write(ln + "\n")

    def _save_turn_legacy(self, user_text: str, assistant_text: str) -> None:
        safe_user = self._escape_newlines(user_text)
        safe_assistant = self._escape_newlines(assistant_text)

        with self._path.open("a", encoding="utf-8") as f:
            f.write(f"USER: {safe_user}\n")
            f.write(f"ASSISTANT: {safe_assistant}\n")
            f.write("---\n")

    def _load_turns_legacy(self) -> list[ChatTurn]:
        turns: list[ChatTurn] = []
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
                    turns.append(ChatTurn(self._unescape_newlines(user), self._unescape_newlines(assistant)))
                user = None
                assistant = None

        return turns

    @staticmethod
    def _escape_newlines(text: str) -> str:
        return ("" if text is None else str(text)).replace("\r\n", "\\n").replace("\n", "\\n")

    @staticmethod
    def _unescape_newlines(text: str) -> str:
        return ("" if text is None else str(text)).replace("\\n", "\n")
