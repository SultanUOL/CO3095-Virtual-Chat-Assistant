from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Deque, List, Optional
from uuid import uuid4

from vca.domain.chat_turn import ChatTurn
from vca.domain.constants import HISTORY_MAX_TURNS


@dataclass(frozen=True)
class Message:
    role: str
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class ClarificationState:
    original_text: str
    options: List[str]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    attempts: int = 0


@dataclass
class ConversationSession:
    session_id: str = field(default_factory=lambda: str(uuid4()))
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    messages: Deque[Message] = field(default_factory=deque)
    pending_clarification: Optional[ClarificationState] = None

    def clear(self) -> None:
        self.messages.clear()
        self.pending_clarification = None

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))

        max_messages = HISTORY_MAX_TURNS * 2
        while len(self.messages) > max_messages:
            self.messages.popleft()

    def recent_messages(self, limit: int = 10) -> List[Message]:
        if limit <= 0:
            return []
        if len(self.messages) <= limit:
            return list(self.messages)
        return list(self.messages)[-limit:]

    def recent_turns(self, limit: int = 3) -> List[ChatTurn]:
        """Return the last completed turns.

        A turn is defined as a user message followed by the next assistant message.
        """
        if limit <= 0:
            return []

        msgs = list(self.messages)
        turns: List[ChatTurn] = []
        i = 0
        while i < len(msgs) - 1:
            m = msgs[i]
            n = msgs[i + 1]
            if m.role == "user" and n.role == "assistant":
                turns.append(ChatTurn(user_text=m.content, assistant_text=n.content))
                i += 2
            else:
                i += 1

        if len(turns) <= limit:
            return turns
        return turns[-limit:]

    def set_pending_clarification(self, original_text: str, options: List[str]) -> None:
        cleaned = [str(o).strip().casefold() for o in options if str(o).strip() != ""]
        dedup: List[str] = []
        for o in cleaned:
            if o not in dedup:
                dedup.append(o)
        self.pending_clarification = ClarificationState(original_text=original_text, options=dedup)

    def clear_pending_clarification(self) -> None:
        self.pending_clarification = None
