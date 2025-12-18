"""
Response generation based on intent and conversation state.
Backbone only.
"""

from __future__ import annotations

from typing import List, Optional

from vca.domain.session import Message


class ResponseGenerator:
    """Generates assistant replies."""
    _ECHO_LIMIT = 200

    def generate(self, intent: str, raw_text: str, recent_messages: Optional[List[Message]] = None) -> str:
        if intent is None:
            safe_intent = "unknown"
        else:
            safe_intent = str(intent)

        if raw_text is None:
            text = ""
        else:
            text = str(raw_text)

        stripped = text.strip()

        if safe_intent == "empty":
            return "Type a message and I will respond. You can also type help."

        if safe_intent == "help":
            return "Commands: help, history, exit. Otherwise type any message to get a basic reply."

        if safe_intent == "history":
            if not recent_messages:
                return "No messages yet in this session."
            last_few = recent_messages[-6:]
            lines = []
            for m in last_few:
                lines.append(f"{m.role}: {m.content}")
            return "Recent messages:\n" + "\n".join(lines)

        if safe_intent == "exit":
            return "Goodbye."

        preview = stripped
        if len(preview) > self._ECHO_LIMIT:
            preview = preview[: self._ECHO_LIMIT] + "..."

        if preview == "":
            return "I did not catch that. Type a message or type help."

        user_count = 0
        if recent_messages:
            for m in recent_messages:
                if m.role == "user":
                    user_count += 1

        if user_count > 0:
            return f"You said: {preview}  Messages this session: {user_count}"
        return f"You said: {preview}"
