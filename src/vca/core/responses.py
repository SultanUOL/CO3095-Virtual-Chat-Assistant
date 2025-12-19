"""vca.core.responses

Response generation based on intent and conversation state.

This module is intentionally separate from intent classification so it can stay
focused on generating replies.
"""

from __future__ import annotations

from typing import List, Optional

from vca.core.intents import Intent
from vca.domain.session import Message


class ResponseGenerator:
    """Generates assistant replies."""
    _ECHO_LIMIT = 200

    @staticmethod
    def _safe_text(raw_text: str | None) -> str:
        return "" if raw_text is None else str(raw_text)

    def _preview(self, text: str) -> str:
        stripped = text.strip()
        if len(stripped) > self._ECHO_LIMIT:
            return stripped[: self._ECHO_LIMIT] + "..."
        return stripped

    def _session_suffix(self, recent_messages: Optional[List[Message]]) -> str:
        user_count = 0
        if recent_messages:
            for m in recent_messages:
                if m.role == "user":
                    user_count += 1
        return f"  Messages this session: {user_count}" if user_count > 0 else ""

    def _normalize_intent(self, intent: Intent | str | None) -> Intent:
        if intent is None:
            return Intent.UNKNOWN
        if isinstance(intent, Intent):
            return intent
        # String based fallback for backward compatibility
        try:
            return Intent(str(intent))
        except ValueError:
            return Intent.UNKNOWN

    def generate(
        self,
        intent: Intent | str | None,
        raw_text: str | None,
        recent_messages: Optional[List[Message]] = None,
    ) -> str:
        resolved_intent = self._normalize_intent(intent)
        text = self._safe_text(raw_text)
        suffix = self._session_suffix(recent_messages)

        if resolved_intent is Intent.EMPTY:
            return "Type a message and I will respond. You can also type help."

        if resolved_intent is Intent.HELP:
            return "Commands: help, history, exit. Otherwise type any message to get a basic reply."

        if resolved_intent is Intent.HISTORY:
            if not recent_messages:
                return "No messages yet in this session."
            last_few = recent_messages[-6:]
            lines = [f"{m.role}: {m.content}" for m in last_few]
            return "Recent messages:\n" + "\n".join(lines)

        if resolved_intent is Intent.EXIT:
            return "Goodbye."

        if resolved_intent is Intent.GREETING:
            return "Hello. Type help to see what I can do." + suffix

        preview = self._preview(text)

        if resolved_intent is Intent.QUESTION:
            if preview == "":
                return "I did not catch your question. Type help for commands."
            return "I think you are asking a question: " + preview + suffix

        if preview == "":
            return "I did not catch that. Type a message or type help."

        return f"You said: {preview}" + suffix

    def fallback(self) -> str:
        return "Sorry, something went wrong. Please try again."
