"""vca.storage.interaction_log_store

File based interaction logging for analysis.

This log is intentionally separate from conversation history and is designed to
store minimal metadata by default.

User story 36 test readiness
The time source can be injected so timestamps are deterministic in tests.
"""

from __future__ import annotations

import datetime as dt
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Protocol, Union, runtime_checkable

from vca.core.intents import Intent


@dataclass(frozen=True)
class InteractionEvent:
    timestamp_utc: str
    input_length: int
    intent: str
    confidence: float
    fallback_used: bool
    processing_time_ms: int
    rule_match_count: int
    multiple_rules_matched: bool


@runtime_checkable
class InteractionLogStoreProtocol(Protocol):
    def append_event(
        self,
        input_length: int,
        intent: Intent | str,
        fallback_used: bool,
        confidence: float = 0.0,
        processing_time_ms: int = 0,
        rule_match_count: int = 0,
        multiple_rules_matched: bool = False,
    ) -> None: ...
    def flush(self) -> None: ...
    def close(self) -> None: ...


class InteractionLogStore:
    DEFAULT_PATH = Path("data") / "interaction_log.jsonl"

    def __init__(
        self,
        path: Union[str, Path, None] = None,
        *,
        now_utc: Callable[[], dt.datetime] | None = None,
    ) -> None:
        self._path = Path(path) if path is not None else self.DEFAULT_PATH
        self._now_utc = now_utc if now_utc is not None else (lambda: dt.datetime.now(tz=dt.timezone.utc))

    @property
    def path(self) -> Path:
        return self._path

    def flush(self) -> None:
        return

    def close(self) -> None:
        return

    def append_event(
        self,
        input_length: int,
        intent: Intent | str,
        fallback_used: bool,
        confidence: float = 0.0,
        processing_time_ms: int = 0,
        rule_match_count: int = 0,
        multiple_rules_matched: bool = False,
    ) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)

        ts = self._now_utc().replace(microsecond=0).strftime("%Y%m%dT%H%M%SZ")

        intent_str = str(intent.value) if hasattr(intent, "value") else str(intent)

        event = InteractionEvent(
            timestamp_utc=ts,
            input_length=max(0, int(input_length)),
            intent=intent_str,
            confidence=max(0.0, min(1.0, float(confidence))),
            fallback_used=bool(fallback_used),
            processing_time_ms=max(0, int(processing_time_ms)),
            rule_match_count=max(0, int(rule_match_count)),
            multiple_rules_matched=bool(multiple_rules_matched),
        )

        line = json.dumps(asdict(event), ensure_ascii=False)
        with self._path.open("a", encoding="utf8") as f:
            f.write(line + "\n")