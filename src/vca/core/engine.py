"""
Core conversation engine.
Coordinates parsing, intent classification, response generation, and persistence.
"""

from __future__ import annotations

import logging

from vca.core.intents import IntentClassifier
from vca.core.responses import ResponseGenerator
from vca.storage.history_store import HistoryStore
from vca.domain.session import ConversationSession
from vca.core.validator import InputValidator

logger = logging.getLogger(__name__)

class ChatEngine:
    """
    Conversation engine with input validation, session handling, and error fallback.
    """

    def __init__(self) -> None:
        self._classifier = IntentClassifier()
        self._responder = ResponseGenerator()
        self._history = HistoryStore()
        self._session = ConversationSession()
        self._validator = InputValidator()

    @property
    def session(self) -> ConversationSession:
        return self._session

    def process_turn(self, raw_text: str) -> str:
        """
        Process one turn. On failure, return a safe fallback response and log the error.
        """
        try:
            clean = self._validator.clean(raw_text)
            text = clean.text

            intent = self._classifier.classify(text)

            self._session.add_message("user", text)

            recent = self._session.recent_messages(limit=10)
            response = self._responder.generate(intent, text, recent_messages=recent)

            if clean.was_truncated:
                response = response + "  Note: your input was truncated."

            self._session.add_message("assistant", response)

            return response

        except Exception:
            logger.exception("Error while processing turn")
            fallback = self._responder.fallback()
            try:
                self._session.add_message("assistant", fallback)
            except Exception:
                pass
            return fallback

    def classify_intent(self, raw_text: str) -> str:
        try:
            clean = self._validator.clean(raw_text)
            return self._classifier.classify(clean.text)
        except Exception:
            logger.exception("Error while classifying intent")
            return "unknown"