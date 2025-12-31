"""
File based storage for chat history.
"""

from __future__ import annotations

import datetime as _dt
import json
import logging
import os
import tempfile
from collections import deque
from pathlib import Path
from typing import Callable, Protocol, Union, runtime_checkable

from vca.domain.chat_turn import ChatTurn
from vca.domain.constants import HISTORY_MAX_TURNS
from vca.storage.file_lock import FileLock, FileLockTimeout

logger = logging.getLogger(__name__)


@runtime_checkable
class HistoryStoreProtocol(Protocol):
    def load_turns(self, max_turns: int | None = None) -> list[ChatTurn]: ...
    def save_turn(self, user_text: str, assistant_text: str) -> None: ...
    def clear_file(self) -> None: ...
    def flush(self) -> None: ...
    def close(self) -> None: ...


class HistoryStore:
    """Stores and loads chat history from disk."""

    DEFAULT_PATH = Path("data") / "history.jsonl"

    def __init__(
        self,
        path: Union[str, Path, None] = None,
        *,
        max_turns: int = HISTORY_MAX_TURNS,
        now_utc: Callable[[], _dt.datetime] | None = None,
    ) -> None:
        self._path = Path(path) if path is not None else self.DEFAULT_PATH
        self._max_turns = int(max_turns) if int(max_turns) > 0 else int(HISTORY_MAX_TURNS)
        self._now_utc = now_utc if now_utc is not None else (lambda: _dt.datetime.now(tz=_dt.timezone.utc))

        # US43: last known good state used when reads happen during a write lock
        self._last_good_turns: list[ChatTurn] = []

    @property
    def path(self) -> Path:
        return self._path

    def flush(self) -> None:
        return

    def close(self) -> None:
        return

    def clear_file(self) -> None:
        """Delete history file if it exists (non fatal)."""
        try:
            if self._path.exists():
                self._path.unlink()
        except Exception as ex:
            logger.exception("History clear failed error_type=%s", type(ex).__name__)
            return



    def save_turn(self, user_text: str, assistant_text: str) -> None:
        """Append one conversation turn to the history file safely."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as ex:
            logger.exception("History directory create failed error_type=%s", type(ex).__name__)
            return

        lock = FileLock(self._path, retries=3, delay_s=0.01)

        try:
            with lock:
                if self._path.suffix.lower() == ".txt":
                    self._save_turn_legacy(user_text, assistant_text)
                    self._trim_file_to_last_n_turns(self._max_turns)
                    return

                user_ts = self._utc_iso()
                assistant_ts = self._utc_iso()

                records = [
                    {"ts": user_ts, "role": "user", "content": "" if user_text is None else str(user_text)},
                    {"ts": assistant_ts, "role": "assistant", "content": "" if assistant_text is None else str(assistant_text)},
                ]

                # newline discipline for JSONL
                with self._path.open("a", encoding="utf-8", newline="\n") as f:
                    for rec in records:
                        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

                self._trim_file_to_last_n_turns(self._max_turns)

        except FileLockTimeout:
            logger.warning("History write skipped file_locked=True path=%s", str(self._path))
            return
        except Exception as ex:
            logger.exception("History save failed error_type=%s", type(ex).__name__)
            return


    def load_turns(self, max_turns: int | None = None) -> list[ChatTurn]:
        """Load persisted conversation turns safely."""
        try:
            if not self._path.exists():
                return []
        except Exception as ex:
            logger.exception("History exists check failed error_type=%s", type(ex).__name__)
            return []

        # If a writer holds the lock, serve last known good state.
        lock = FileLock(self._path, retries=1, delay_s=0.0)
        if not lock.try_acquire():
            logger.warning("History read served from cache file_locked=True path=%s", str(self._path))
            return list(self._last_good_turns)

        try:
            if self._path.suffix.lower() == ".txt":
                try:
                    turns = self._load_turns_legacy()
                    self._last_good_turns = list(turns)
                    return turns
                except Exception as ex:
                    logger.error("History file is corrupted legacy format starting with empty history", exc_info=ex)
                    return []

            try:
                effective_max_turns = self._max_turns if max_turns is None else max_turns

                if effective_max_turns is None or effective_max_turns <= 0:
                    lines = self._stream_all_lines()
                else:
                    lines = self._stream_last_lines(max_lines=int(effective_max_turns) * 2)
            except Exception as ex:
                logger.error("Failed to read history file starting with empty history", exc_info=ex)
                return []

            records: list[tuple[str, str, str | None]] = []
            corruption_detected = False

            for line in lines:
                if not line.strip():
                    continue

                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as ex:
                    logger.error("History file is corrupted invalid JSON starting with empty history", exc_info=ex)
                    corruption_detected = True
                    break
                except Exception as ex:
                    logger.error("History parse failed starting with empty history", exc_info=ex)
                    corruption_detected = True
                    break

                if not isinstance(obj, dict):
                    logger.error("History file is corrupted non object JSON starting with empty history")
                    corruption_detected = True
                    break

                role = str(obj.get("role", "")).strip().lower()
                if role not in ("user", "assistant"):
                    logger.error("History file is corrupted invalid role starting with empty history")
                    corruption_detected = True
                    break

                content = obj.get("content", "")
                ts = obj.get("ts")

                ts_str: str | None
                if ts is None:
                    ts_str = None
                else:
                    ts_str = str(ts)

                records.append((role, "" if content is None else str(content), ts_str))

            if corruption_detected:
                return []

            turns: list[ChatTurn] = []
            pending_user_text: str | None = None
            pending_user_ts: str | None = None

            for role, content, ts in records:
                if role == "user":
                    pending_user_text = content
                    pending_user_ts = ts
                elif role == "assistant":
                    if pending_user_text is not None:
                        turns.append(
                            ChatTurn(
                                user_text=pending_user_text,
                                assistant_text=content,
                                user_ts=pending_user_ts,
                                assistant_ts=ts,
                            )
                        )
                        pending_user_text = None
                        pending_user_ts = None

            # US43: update last known good only on successful parse
            self._last_good_turns = list(turns)
            return turns

        finally:
            lock.release()

    def load_history(self) -> list[str]:
        """Load full file lines (kept for trimming and test support)."""
        try:
            if not self._path.exists():
                return []
        except Exception as ex:
            logger.exception("History exists check failed error_type=%s", type(ex).__name__)
            return []

        try:
            with self._path.open("r", encoding="utf-8") as f:
                return [line.rstrip("\n") for line in f.readlines()]
        except Exception as ex:
            logger.exception("History read failed error_type=%s", type(ex).__name__)
            return []

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

    def _utc_iso(self) -> str:
        return self._now_utc().replace(microsecond=0).isoformat()

    def _atomic_rewrite_lines(self, lines: list[str]) -> None:
        """Atomically rewrite the history file with the given lines."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as ex:
            logger.exception("History directory create failed error_type=%s", type(ex).__name__)
            return

        tmp_path: Path | None = None
        try:
            fd, tmp_name = tempfile.mkstemp(prefix=self._path.name + ".tmp.", dir=str(self._path.parent))
            tmp_path = Path(tmp_name)

            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
                for ln in lines:
                    f.write(str(ln) + "\n")
                f.flush()
                try:
                    os.fsync(f.fileno())
                except Exception:
                    pass

            tmp_path.replace(self._path)

        except Exception as ex:
            logger.exception("History atomic rewrite failed error_type=%s", type(ex).__name__)
            try:
                if tmp_path is not None and tmp_path.exists():
                    tmp_path.unlink()
            except Exception:
                pass

    def _trim_file_to_last_n_turns(self, max_turns: int) -> None:
        """Keep only the most recent N turns in the file."""
        try:
            if not self._path.exists():
                return
        except Exception as ex:
            logger.exception("History exists check failed error_type=%s", type(ex).__name__)
            return

        try:
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
                self._atomic_rewrite_lines(flat)
                return

            if max_turns <= 0:
                self._atomic_rewrite_lines([])
                return

            max_lines = max_turns * 2
            keep_lines = self._stream_last_lines(max_lines=max_lines)
            self._atomic_rewrite_lines(keep_lines)

        except Exception as ex:
            logger.exception("History trim failed error_type=%s", type(ex).__name__)
            return

    # ---------------- Legacy format ----------------

    def _save_turn_legacy(self, user_text: str, assistant_text: str) -> None:
        safe_user = self._escape_newlines(user_text)
        safe_assistant = self._escape_newlines(assistant_text)

        with self._path.open("a", encoding="utf-8", newline="\n") as f:
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
