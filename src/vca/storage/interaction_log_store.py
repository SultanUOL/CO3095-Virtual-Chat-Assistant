"""vca.storage.interaction_log_store

File based interaction logging for analysis.

This log is intentionally separate from conversation history and is designed to
store minimal metadata by default.
"""

from __future__ import annotations

import datetime as dt
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional, Union

from vca.core.intents import Intent


@dataclass(frozen=True)
class InteractionEvent:
    """Minimal metadata about one user turn."""

    timestamp_utc: str
    input_length: int
    intent: str
    confidence: float
    fallback_used: bool


class InteractionLogStore:
    """Append only JSON lines log for interaction analytics."""

    DEFAULT_PATH = Path("data") / "interaction_log.jsonl"

    def __init__(self, path: Union[str, Path, None] = None) -> None:
        self._path = Path(path) if path is not None else self.DEFAULT_PATH

    @property
    def path(self) -> Path:
        return self._path

    def append_event(
        self,
        input_length: int,
        intent: Intent | str,
        fallback_used: bool,
        confidence: float = 0.0,
    ) -> None:
        """Append one interaction event.

        This stores minimal metadata only and never stores user content.
        """
        self._path.parent.mkdir(parents=True, exist_ok=True)

        ts = dt.datetime.now(tz=dt.timezone.utc).replace(microsecond=0).strftime("%Y%m%dT%H%M%SZ")

        if hasattr(intent, "value"):
            intent_str = str(intent.value)
        else:
            intent_str = str(intent)

        event = InteractionEvent(
            timestamp_utc=ts,
            input_length=max(0, int(input_length)),
            intent=intent_str,
            confidence=max(0.0, min(1.0, float(confidence))),
            fallback_used=bool(fallback_used),
        )

        line = json.dumps(asdict(event), ensure_ascii=False)
        with self._path.open("a", encoding="utf8") as f:
            f.write(line + "\n")
