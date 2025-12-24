"""vca.core.engine

Core conversation engine.

Coordinates validation, intent classification, response generation, and session
persistence. This module should not contain intent rules or response text beyond
safe fallbacks.
"""

from __future__ import annotations

import logging
import time

from vca.core.intents import Intent, IntentClassifier
from vca.core.responses import ResponseGenerator
from vca.core.validator import InputValidator
from vca.domain.session import ConversationSession
from vca.storage.history_store import HistoryStore
from vca.storage.interaction_log_store import InteractionLogStore

logger = logging.getLogger(__name__)
error_logger = logging.getLogger("vca.errors")

CONFIDENCE_THRESHOLD = 0.65


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
        effective_intent: Intent | str = Intent.UNKNOWN
        confidence = 0.0
        fallback_used = False

        started = time.perf_counter()

        try:
            clean = self._validator.clean(raw_text)
            text = clean.text
            input_length = len(text)

            if self._session.pending_clarification is not None:
                state = self._session.pending_clarification
                choice = self._parse_clarification_choice(text, state.options)

                self._session.add_message("user", text)
                recent = self._session.recent_messages(limit=10)

                if choice is None:
                    self._session.clear_pending_clarification()
                    effective_intent = Intent.UNKNOWN
                    response = self._responder.route("unknown")(text, recent)
                else:
                    self._session.clear_pending_clarification()
                    effective_intent = choice
                    handler = self.route_intent(choice)
                    response = handler(state.original_text, recent)

                if clean.was_truncated:
                    response = response + "  Note: your input was truncated."

                self._session.add_message("assistant", response)

                try:
                    self._history.save_turn(text, response)
                except Exception as ex:
                    logger.warning("History save failed (non fatal): %s", ex)
                    try:
                        error_logger.exception(
                            "History save failed error_type=%s intent=%s file_operation=True",
                            type(ex).__name__,
                            str(effective_intent),
                        )
                    except Exception:
                        pass

                return response

            try:
                intent = self._classifier.classify(text)
            except Exception as ex:
                fallback_used = True
                intent = Intent.UNKNOWN
                effective_intent = intent
                confidence = 0.0

                try:
                    error_logger.exception(
                        "Error while classifying intent error_type=%s intent=%s file_operation=False",
                        type(ex).__name__,
                        str(effective_intent),
                    )
                except Exception:
                    logger.exception("Error while classifying intent error_type=%s", type(ex).__name__)

                return "Sorry, something went wrong. Please try again."

            effective_intent = intent

            result = getattr(self._classifier, "last_result", None)
            if result is not None:
                try:
                    confidence = float(result.confidence)
                except Exception:
                    confidence = 0.0
            else:
                confidence = 1.0 if intent != Intent.UNKNOWN else confidence

            logger.debug(
                "Intent confidence intent=%s confidence=%.2f",
                getattr(intent, "value", str(intent)),
                confidence,
            )

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
                    pass

            self._session.add_message("user", text)
            recent = self._session.recent_messages(limit=10)

            faq = self._responder.faq_response_for(text)
            if faq is not None:
                response = faq
            else:
                should_clarify = False

                if confidence < CONFIDENCE_THRESHOLD and intent not in (Intent.EMPTY, Intent.UNKNOWN):
                    should_clarify = True
                    logger.info(
                        "Low confidence intent starting clarification flow intent=%s",
                        getattr(intent, "value", str(intent)),
                    )

                if self._is_vague_unknown(text, intent):
                    should_clarify = True
                    logger.info("Vague unknown input starting clarification flow")

                if should_clarify:
                    fallback_used = True

                    candidates = []
                    if result is not None:
                        candidates = getattr(result, "candidates", []) or []
                    elif decision is not None:
                        candidates = getattr(decision, "candidates", []) or []

                    options = self._clarification_options_from_candidates(candidates)
                    self._session.set_pending_clarification(original_text=text, options=options)
                    response = self._responder.generate_clarifying_question(options)

                    effective_intent = "clarify"
                else:
                    handler = self.route_intent(effective_intent)
                    response = handler(text, recent)

            if clean.was_truncated:
                response = response + "  Note: your input was truncated."

            self._session.add_message("assistant", response)

            try:
                self._history.save_turn(text, response)
            except Exception as ex:
                logger.warning("History save failed (non fatal): %s", ex)
                try:
                    error_logger.exception(
                        "History save failed error_type=%s intent=%s file_operation=True",
                        type(ex).__name__,
                        str(effective_intent),
                    )
                except Exception:
                    pass

            return response

        except Exception as ex:
            fallback_used = True

            try:
                error_logger.exception(
                    "Error while processing turn error_type=%s intent=%s file_operation=False",
                    type(ex).__name__,
                    str(effective_intent),
                )
            except Exception:
                logger.exception("Error while processing turn error_type=%s", type(ex).__name__)

            fallback = self._responder.fallback()
            try:
                self._session.add_message("assistant", fallback)
            except Exception:
                pass
            return fallback

        finally:
            try:
                elapsed_ms = int((time.perf_counter() - started) * 1000)
                self._interaction_log.append_event(
                    input_length=input_length,
                    intent=effective_intent,
                    fallback_used=fallback_used,
                    confidence=confidence,
                    processing_time_ms=elapsed_ms,
                )
            except Exception as ex:
                logger.warning("Interaction log failed (non fatal): %s", ex)

    def classify_intent(self, text: str) -> Intent:
        """Classify user intent with safe fallback on failure."""
        try:
            return self._classifier.classify(text)
        except Exception as ex:
            try:
                error_logger.exception(
                    "Error while classifying intent error_type=%s intent=%s file_operation=False",
                    type(ex).__name__,
                    "unknown",
                )
            except Exception:
                logger.exception("Error while classifying intent error_type=%s", type(ex).__name__)
            return Intent.UNKNOWN

    def route_intent(self, intent):
        """Return the handler function for a given intent."""
        if hasattr(intent, "value"):
            return self._responder.route(intent.value)
        return self._responder.route(intent)

    def _clarification_options_from_candidates(self, candidates) -> list[str]:
        order = ["exit", "help", "history", "thanks", "goodbye", "greeting", "question"]
        seen: set[str] = set()
        found: list[str] = []

        for item in candidates or []:
            cand_intent = item[0]
            value = cand_intent.value if hasattr(cand_intent, "value") else str(cand_intent)
            key = str(value).strip().casefold()
            if key in ("unknown", "empty"):
                continue
            if key not in seen:
                seen.add(key)
                found.append(key)

        found.sort(key=lambda x: order.index(x) if x in order else 999)

        if len(found) >= 2:
            return found[:2]

        return ["help", "question"]

    def _parse_clarification_choice(self, text: str, options: list[str]) -> str | None:
        lower = (text or "").strip().casefold()

        if lower in {"1", "one"}:
            return options[0] if len(options) >= 1 else None
        if lower in {"2", "two"}:
            return options[1] if len(options) >= 2 else None

        if lower in options:
            return lower

        if "exit" in options and lower in {"quit", "bye", "goodbye"}:
            return "exit"

        if "help" in options and lower in {"h", "commands", "help"}:
            return "help"

        if "question" in options and lower in {"question"}:
            return "question"

        return None

    def _is_vague_unknown(self, text: str, intent) -> bool:
        stripped = (text or "").strip()
        intent_value = str(intent.value) if hasattr(intent, "value") else str(intent)

        if intent_value.strip().casefold() != "unknown":
            return False

        short = len(stripped) <= 3
        one_word = len(stripped.split()) <= 1
        return short and one_word