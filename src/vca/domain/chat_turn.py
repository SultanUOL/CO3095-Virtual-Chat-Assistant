from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChatTurn:
    user_text: str
    assistant_text: str

    def to_dict(self) -> dict[str, str]:
        """Serialise this turn into a JSON-friendly dict."""
        return {"user_text": self.user_text, "assistant_text": self.assistant_text}

    @staticmethod
    def from_dict(data: dict[str, str]) -> "ChatTurn":
        """De-serialise a turn from a dict."""
        return ChatTurn(
            user_text=str(data.get("user_text", "")),
            assistant_text=str(data.get("assistant_text", "")),
        )
