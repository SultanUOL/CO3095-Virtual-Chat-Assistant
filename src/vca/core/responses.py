"""vca.core.responses

Response generation based on intent and conversation state.

This module is intentionally separate from intent classification so it can stay
focused on generating replies. The generator routes resolved intents to per intent
handler methods to keep behaviour explicit and testable.

It also includes a small deterministic FAQ lookup. FAQ matching is done via a
normalization function so the same input always produces the same FAQ key.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional

from vca.core.intents import Intent
from vca.domain.session import Message

Handler = Callable[[str, Optional[List[Message]]], str]


class ResponseGenerator:
    """Generates assistant replies by routing intents to handler methods plus FAQ lookup."""

    _ECHO_LIMIT = 200

    _FAQ_MAP: Dict[str, str] = {
        "help": "Commands: help, history, exit. You can also type a message to get a basic reply.",
        "what can you do": "I can respond to greetings and questions, show session history, and explain commands. Type help.",
        "who are you": "I am a virtual chat assistant built for coursework as a simple deterministic CLI assistant.",
        "how do i exit": "Type exit or quit to close the assistant.",
        "how is history stored": "History is stored in memory for this session only. It is not saved between runs yet.",
    }

    def generate(self, intent: str, raw_text: str, recent_messages: Optional[List[Message]] = None) -> str:
        faq = self.faq_response_for(raw_text)
        if faq is not None:
            return faq

        text = "" if raw_text is None else str(raw_text)
        handler = self.route(intent)
        return handler(text, recent_messages)

    def route(self, intent: Intent) -> Handler:
        handlers: Dict[Intent, Handler] = {
            Intent.EMPTY: self.handle_empty,
            Intent.HELP: self.handle_help,
            Intent.HISTORY: self.handle_history,
            Intent.EXIT: self.handle_exit,
            Intent.GREETING: self.handle_greeting,
            Intent.QUESTION: self.handle_question,
            Intent.UNKNOWN: self.handle_unknown,
        }
        return handlers.get(intent, self.handle_unknown)

    def _normalize_intent(self, intent: Intent | str | None) -> Intent:
        if intent is None:
            return Intent.UNKNOWN
        if isinstance(intent, Intent):
            return intent
        try:
            return Intent(str(intent))
        except ValueError:
            return Intent.UNKNOWN

    def normalize_faq_key(self, raw_text: str | None) -> str:
        text = "" if raw_text is None else str(raw_text)
        key = text.strip().casefold()
        if key.endswith("?"):
            key = key[:-1].strip()
        return key

    def faq_response_for(self, raw_text: str | None) -> Optional[str]:
        key = self.normalize_faq_key(raw_text)
        if key == "":
            return None
        return self._FAQ_MAP.get(key)

    def handle_empty(self, _text: str, _recent: Optional[List[Message]]) -> str:
        return "Type a message and I will respond. You can also type help."

    def handle_help(self, _text: str, _recent: Optional[List[Message]]) -> str:
        return "Commands: help, history, exit. Otherwise type any message to get a basic reply."

    def handle_history(self, _text: str, recent: Optional[List[Message]]) -> str:
        if not recent:
            return "No messages yet in this session."
        last_few = recent[-6:]
        lines = [f"{m.role}: {m.content}" for m in last_few]
        return "Recent messages:\n" + "\n".join(lines)

    def handle_exit(self, _text: str, _recent: Optional[List[Message]]) -> str:
        return "Goodbye."

    def handle_greeting(self, _text: str, recent: Optional[List[Message]]) -> str:
        return "Hello. Type help to see what I can do." + self._session_suffix(recent)

    def handle_question(self, text: str, recent: Optional[List[Message]]) -> str:
        preview = self._preview(text)
        if preview == "":
            return "I did not catch your question. Type help for commands."
        return "I think you are asking a question: " + preview + self._session_suffix(recent)

    def handle_unknown(self, text: str, recent: Optional[List[Message]]) -> str:
        preview = self._preview(text)
        if preview == "":
            return "I did not catch that. Type a message or type help."
        return "You said: " + preview + self._session_suffix(recent)

    def _preview(self, text: str) -> str:
        stripped = (text or "").strip()
        if len(stripped) > self._ECHO_LIMIT:
            return stripped[: self._ECHO_LIMIT] + "..."
        return stripped

    def _session_suffix(self, recent: Optional[List[Message]]) -> str:
        user_count = 0
        if recent:
            for m in recent:
                if m.role == "user":
                    user_count += 1
        return f"  Messages this session: {user_count}" if user_count > 0 else ""

    def fallback(self) -> str:
        return "Sorry, something went wrong. Please try again."
