from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Deque, List
from uuid import uuid4
from collections import deque
from vca.domain.constants import HISTORY_MAX_TURNS


@dataclass(frozen=True)
class Message:
    role: str
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ConversationSession:
    session_id: str = field(default_factory=lambda: str(uuid4()))
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    messages: Deque[Message] = field(default_factory=deque)

    def clear(self) -> None:
        self.messages.clear()

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))

        # US11: trim oldest turns if limit exceeded
        max_messages = HISTORY_MAX_TURNS * 2
        while len(self.messages) > max_messages:
            self.messages.popleft()

    def recent_messages(self, limit: int = 10) -> List[Message]:
        if limit <= 0:
            return []
        if len(self.messages) <= limit:
            return list(self.messages)
        return list(self.messages)[-limit:]
