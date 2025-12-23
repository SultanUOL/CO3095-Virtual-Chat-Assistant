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
from vca.storage.interaction_log_store import InteractionLogStore

logger = logging.getLogger(__name__)


class ChatEngine:
    """Conversation engine with input validation, session handling, and error fallback."""

    def __init__(
        self,
        history: HistoryStore | None = None,
        interaction_log: InteractionLogStore | None = None,
    ) -> None:
        self._classifier = IntentClassifier()
        self._responder = ResponseGenerator()
        self._history = history if history is not None else HistoryStore()
        self._interaction_log = interaction_log if interaction_log is not None else InteractionLogStore()
        self._session = ConversationSession()
        self._validator = InputValidator()
        self._loaded_turns_count = 0

        if history is not None:
            try:
                turns = self._history.load_turns()
                for t in turns:
                    self._session.add_message("user", t.user_text)
                    self._session.add_message("assistant", t.assistant_text)
                self._loaded_turns_count = len(turns)
            except Exception as ex:
                logger.warning("History load failed (non fatal): %s", ex)
                self._loaded_turns_count = 0

    def reset_session(self) -> None:
        """Clear in memory conversation state."""
        try:
            self._session.clear()
        except Exception:
            pass

    def clear_history(self, clear_file: bool = True) -> None:
        """Clear session memory and optionally delete persisted history."""
        self.reset_session()
        if clear_file:
            try:
                self._history.clear_file()
            except Exception:
                pass

    @property
    def session(self) -> ConversationSession:
        return self._session

    @property
    def loaded_turns_count(self) -> int:
        return self._loaded_turns_count

    def process_turn(self, raw_text: str | None) -> str:
        """Process one user turn and return the assistant response.

        On failure, returns a safe fallback response and logs the error.
        """
        input_length = 0
        intent: Intent = Intent.UNKNOWN
        fallback_used = False

        try:
            clean = self._validator.clean(raw_text)
            text = clean.text
            input_length = len(text)

            # Important: do not swallow classifier exceptions here.
            # If classification fails, the engine must return the safe fallback response.
            try:
                intent = self._classifier.classify(text)
            except Exception as ex:
                logger.exception(
                    "Error while classifying intent error_type=%s",
                    type(ex).__name__,
                )
                raise

            # Tiny change: if the classifier exposes debug metadata, log it.
            decision = getattr(self._classifier, "last_decision", None)
            if decision is not None:
                try:
                    logger.debug(
                        "Intent selected intent=%s rule=%s candidates=%s",
                        decision.intent.value,
                        decision.rule,
                        [i.value for i, _r in decision.candidates],
                    )
                except Exception:
                    # Never let optional debug logging affect runtime behaviour.
                    pass

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
                logger.warning("History save failed (non fatal): %s", ex)

            return response

        except Exception as ex:
            logger.exception(
                "Error while processing turn error_type=%s",
                type(ex).__name__,
            )
            fallback_used = True
            fallback = self._responder.fallback()
            try:
                self._session.add_message("assistant", fallback)
            except Exception:
                pass
            return fallback

        finally:
            try:
                self._interaction_log.append_event(
                    input_length=input_length,
                    intent=intent,
                    fallback_used=fallback_used,
                )
            except Exception as ex:
                logger.warning("Interaction log failed (non fatal): %s", ex)

    def classify_intent(self, text: str) -> Intent:
        """Classify user intent with safe fallback on failure.

        This helper is intended for debugging or tests where you want a best effort intent.
        The main engine flow in process_turn must not use this helper, so dependency failures
        still trigger the safe fallback response.
        """
        try:
            return self._classifier.classify(text)
        except Exception as ex:
            logger.exception(
                "Error while classifying intent error_type=%s",
                type(ex).__name__,
            )
            return Intent.UNKNOWN

    def route_intent(self, intent):
        """Return the handler function for a given intent."""
        if hasattr(intent, "value"):
            return self._responder.route(intent.value)
        return self._responder.route(intent)
