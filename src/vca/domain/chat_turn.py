from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChatTurn:
    """Represents one complete conversation turn (user message + assistant response).

    Attributes:
        user_text: The user's message text
        assistant_text: The assistant's response text
        user_ts: Optional timestamp when the user message was created (ISO format)
        assistant_ts: Optional timestamp when the assistant response was created (ISO format)
    """

    user_text: str
    assistant_text: str
    user_ts: str | None = None
    assistant_ts: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        """Convert the ChatTurn to a dictionary representation.

        Returns:
            Dictionary with keys: user_text, assistant_text, user_ts, assistant_ts
        """
        return {
            "user_text": self.user_text,
            "assistant_text": self.assistant_text,
            "user_ts": self.user_ts,
            "assistant_ts": self.assistant_ts,
        }

    @staticmethod
    def from_dict(data: dict) -> "ChatTurn":
        """Create a ChatTurn from a dictionary representation.

        Args:
            data: Dictionary with keys: user_text, assistant_text, user_ts, assistant_ts

        Returns:
            New ChatTurn instance with values from the dictionary
        """
        return ChatTurn(
            user_text=str(data.get("user_text", "")),
            assistant_text=str(data.get("assistant_text", "")),
            user_ts=data.get("user_ts"),
            assistant_ts=data.get("assistant_ts"),
        )
