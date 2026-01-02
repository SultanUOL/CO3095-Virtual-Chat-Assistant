from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChatTurn:
    """
    Represents one user+assistant turn."""

    user_text: str
    assistant_text: str
    user_ts: str | None = None
    assistant_ts: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return {
            "user_text": self.user_text,
            "assistant_text": self.assistant_text,
            "user_ts": self.user_ts,
            "assistant_ts": self.assistant_ts,
        }

    @staticmethod
    def from_dict(data: dict) -> "ChatTurn":
        return ChatTurn(
            user_text=str(data.get("user_text", "")),
            assistant_text=str(data.get("assistant_text", "")),
            user_ts=data.get("user_ts"),
            assistant_ts=data.get("assistant_ts"),
        )
