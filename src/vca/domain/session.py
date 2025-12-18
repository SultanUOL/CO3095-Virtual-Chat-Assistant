from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Deque, List
from collections import deque
from uuid import uuid4


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

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))

    def recent_messages(self, limit: int = 10) -> List[Message]:
        if limit <= 0:
            return []
        if len(self.messages) <= limit:
            return list(self.messages)
        return list(self.messages)[-limit:]
