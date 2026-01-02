"""vca.core.responses

Response generation based on intent and conversation state.

User story 17
Responses consider recent turns in a deterministic way.

User story 18
Earlier conversation turns can influence replies in a safe concise way.

User story 20
Fallback responses are more helpful and consistent.
Unknown intent fallback differs from error fallback.
Fallback text is centralised in this module.
"""

from __future__ import annotations

import re
from typing import Callable, Dict, List, Optional

from vca.core.intents import Intent
from vca.domain.chat_turn import ChatTurn
from vca.domain.session import Message

Handler = Callable[..., str]


class ResponseGenerator:
    _ECHO_LIMIT = 200

    # US20 centralised fallback text
    _FALLBACK_UNKNOWN = (
        "I did not understand that. Please rephrase your message or type help."
    )
    _FALLBACK_ERROR = "Sorry, something went wrong. Please try again."

    _FAQ_MAP: Dict[str, str] = {
        "help": "Commands: help, history, exit. You can also type a message to get a basic reply.",
        "what can you do": "I can respond to greetings and questions, show session history, and explain commands. Type help.",
        "who are you": "I am a virtual chat assistant built for coursework as a simple deterministic CLI assistant.",
        "how do i exit": "Type exit or quit to close the assistant.",
        "how is history stored": "History is stored in a text file at data/history.txt (appended after each turn).",
    }

    def generate(
        self,
        intent: Intent | str | None,
        raw_text: str | None,
        recent_messages: Optional[List[Message]] = None,
        context_turns: Optional[List[ChatTurn]] = None,
    ) -> str:
        faq = self.faq_response_for(raw_text)
        if faq is not None:
            return faq

        resolved_intent = self._normalize_intent(intent)
        text = "" if raw_text is None else str(raw_text)

        handler = self.route(resolved_intent)
        return self._invoke(handler, text, recent_messages, context_turns)

    def route(self, intent) -> Handler:
        if intent is None:
            safe_intent = "unknown"
        elif hasattr(intent, "value"):
            safe_intent = str(intent.value)
        else:
            safe_intent = str(intent)

        safe_intent = safe_intent.strip().casefold()

        handlers: Dict[str, Handler] = {
            "empty": self.handle_empty,
            "help": self.handle_help,
            "history": self.handle_history,
            "exit": self.handle_exit,
            "greeting": self.handle_greeting,
            "question": self.handle_question,
            "thanks": self.handle_thanks,
            "goodbye": self.handle_goodbye,
            "ambiguous": self.handle_ambiguous,
            "unknown": self.handle_unknown,
        }

        return handlers.get(safe_intent, self.handle_unknown)

    def _invoke(
        self,
        handler: Handler,
        text: str,
        recent: Optional[List[Message]],
        context: Optional[List[ChatTurn]],
    ) -> str:
        # Important: some tests monkeypatch handlers that accept only 2 args
        # So we try 3 args first, then retry with 2 args if needed
        try:
            return handler(text, recent, context)
        except TypeError:
            return handler(text, recent)

    def _normalize_intent(self, intent: Intent | str | None) -> Intent:
        if intent is None:
            return Intent.UNKNOWN
        if isinstance(intent, Intent):
            return intent
        try:
            return Intent(str(intent).strip().casefold())
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

    def _previous_user_message_from_recent(
        self, recent: Optional[List[Message]]
    ) -> str:
        if not recent:
            return ""
        earlier = recent[:-1]
        for m in reversed(earlier):
            if m.role == "user":
                return m.content
        return ""

    # Keep this exact method name because your tests reference it
    def extract_topic_from_last_user_message(self, text: str) -> str:
        if not text:
            return ""

        ignore_capitalised = {
            "I",
            "Tell",
            "Please",
            "Can",
            "Could",
            "Would",
            "Should",
            "Do",
            "Does",
            "Did",
            "What",
            "Where",
            "When",
            "Why",
            "How",
        }

        proper_nouns = re.findall(r"\b[A-Z][a-zA-Z]+\b", text)
        for w in proper_nouns:
            if w in ignore_capitalised:
                continue
            if len(w) > 2:
                return w.lower()

        lowered = text.strip().lower()

        m = re.search(r"\babout\s+([a-z0-9]+)\b", lowered)
        if m:
            return m.group(1)

        m = re.search(r"\bregarding\s+([a-z0-9]+)\b", lowered)
        if m:
            return m.group(1)

        cleaned = re.sub(r"[^a-z0-9\s]", " ", lowered)
        words = [w for w in cleaned.split() if w]
        if not words:
            return ""

        stop_words = {
            "i",
            "you",
            "we",
            "they",
            "it",
            "is",
            "are",
            "was",
            "were",
            "the",
            "a",
            "an",
            "to",
            "for",
            "of",
            "on",
            "in",
            "and",
            "what",
            "where",
            "when",
            "why",
            "how",
            "tell",
            "me",
            "about",
            "regarding",
            "please",
            "can",
            "could",
            "would",
            "should",
            "do",
            "does",
            "did",
            "am",
            "im",
            "be",
            "been",
            "being",
            "want",
            "need",
            "like",
            "visiting",
            "going",
            "this",
            "that",
            "these",
            "those",
        }

        for w in words:
            if w not in stop_words and len(w) > 2:
                return w

        return words[0]

    def handle_empty(
        self,
        _text: str,
        _recent: Optional[List[Message]],
        _context: Optional[List[ChatTurn]] = None,
    ) -> str:
        return "Type a message and I will respond. You can also type help."

    def handle_help(
        self,
        _text: str,
        _recent: Optional[List[Message]],
        _context: Optional[List[ChatTurn]] = None,
    ) -> str:
        return "Commands: help, history, exit. Otherwise type any message to get a basic reply."

    def handle_history(
        self,
        _text: str,
        recent: Optional[List[Message]],
        _context: Optional[List[ChatTurn]] = None,
    ) -> str:
        if not recent:
            return "No messages yet in this session."
        last_few = recent[-6:]
        lines = [f"{m.role}: {m.content}" for m in last_few]
        return "Recent messages:\n" + "\n".join(lines)

    def handle_exit(
        self,
        _text: str,
        _recent: Optional[List[Message]],
        _context: Optional[List[ChatTurn]] = None,
    ) -> str:
        return "Goodbye."

    def handle_greeting(
        self,
        _text: str,
        recent: Optional[List[Message]],
        _context: Optional[List[ChatTurn]] = None,
    ) -> str:
        return "Hello. Type help to see what I can do." + self._session_suffix(recent)

    def handle_question(
        self,
        text: str,
        recent: Optional[List[Message]],
        context: Optional[List[ChatTurn]] = None,
    ) -> str:
        preview = self._preview(text)
        if preview == "":
            return "I did not catch your question. Type help for commands."

        # Prefer recent messages because it always exists in engine flow
        previous_user_text = self._previous_user_message_from_recent(recent)

        # Fall back to context if recent was not provided
        if previous_user_text == "" and context:
            previous_user_text = context[-1].user_text

        if previous_user_text:
            topic = self.extract_topic_from_last_user_message(previous_user_text)
            if topic:
                return (
                    "Following up on your earlier message about "
                    + topic
                    + ": "
                    + preview
                    + self._session_suffix(recent)
                )

        return (
            "I think you are asking a question: "
            + preview
            + self._session_suffix(recent)
        )

    def handle_thanks(
        self,
        _text: str,
        _recent: Optional[List[Message]],
        _context: Optional[List[ChatTurn]] = None,
    ) -> str:
        return "You are welcome."

    def handle_goodbye(
        self,
        _text: str,
        _recent: Optional[List[Message]],
        _context: Optional[List[ChatTurn]] = None,
    ) -> str:
        return "Goodbye."

    def handle_ambiguous(
        self,
        _text: str,
        _recent: Optional[List[Message]],
        _context: Optional[List[ChatTurn]] = None,
    ) -> str:
        return "I am not fully sure what you meant. Please rephrase, or type help to see commands."

    def handle_unknown(
        self,
        _text: str,
        _recent: Optional[List[Message]],
        _context: Optional[List[ChatTurn]] = None,
    ) -> str:
        return self.fallback_unknown()

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

    def fallback_unknown(self) -> str:
        return self._FALLBACK_UNKNOWN

    def fallback_error(self) -> str:
        return self._FALLBACK_ERROR

    def fallback(self) -> str:
        return self.fallback_error()

    def generate_clarifying_question(self, options: List[str]) -> str:
        cleaned = [str(o).strip().casefold() for o in options if str(o).strip() != ""]
        if len(cleaned) < 2:
            cleaned = ["help", "question"]

        opt1 = cleaned[0]
        opt2 = cleaned[1]

        return (
            "I am not fully sure what you meant. "
            f"Did you mean {opt1} or {opt2}? "
            f"Reply 1 for {opt1} or Reply 2 for {opt2}."
        )

    def route_intent(self, intent) -> Handler:
        return self.route(intent)
