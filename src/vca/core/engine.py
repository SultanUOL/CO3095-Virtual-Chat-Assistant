"""vca.core.engine

Core conversation engine.

Coordinates validation, intent classification, response generation, and session
persistence. This module should not contain intent rules or response text beyond
safe fallbacks.
"""

from __future__ import annotations

import logging

from vca.core.intents import Intent, IntentClassifier
from vca.core.responses import ResponseGenerator
from vca.core.validator import InputValidator
from vca.domain.session import ConversationSession
from vca.storage.history_store import HistoryStore

logger = logging.getLogger(__name__)


class ChatEngine:
    """Conversation engine with input validation, session handling, and error fallback."""

    def __init__(self) -> None:
        self._classifier = IntentClassifier()
        self._responder = ResponseGenerator()
        self._history = HistoryStore()
        self._session = ConversationSession()
        self._validator = InputValidator()

    @property
    def session(self) -> ConversationSession:
        return self._session

    def process_turn(self, raw_text: str | None) -> str:
        """Process one user turn and return the assistant response.

        On failure, returns a safe fallback response and logs the error.
        """
        try:
            clean = self._validator.clean(raw_text)
            text = clean.text

            intent = self._classifier.classify(text)

            self._session.add_message("user", text)

            recent = self._session.recent_messages(limit=10)

            faq = self._responder.faq_response_for(text)
            if faq is not None:
                response = faq
            else:
                handler = self.route_intent(intent)
                response = handler(text, recent)

            if clean.was_truncated:
                response = response + "  Note: your input was truncated."

            self._session.add_message("assistant", response)
            try:
                self._history.save_turn(text, response)
            except Exception as ex:
                logger.warning("History save failed (non-fatal): %s", ex)
            return response

        except Exception:
            logger.exception("Error while processing turn")
            fallback = self._responder.fallback()
            try:
                self._session.add_message("assistant", fallback)
            except Exception:
                pass
            return fallback

    def classify_intent(self, raw_text: str | None) -> Intent:
        """Classify intent only.

        Useful for unit tests and for debugging the classifier without generating a reply.
        """
        try:
            clean = self._validator.clean(raw_text)
            return self._classifier.classify(clean.text)
        except Exception:
            logger.exception("Error while classifying intent")
            return Intent.UNKNOWN

    def route_intent(self, intent):
        if hasattr(intent, "value"):
            return self._responder.route(intent.value)
        return self._responder.route(intent)

