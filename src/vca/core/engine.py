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

CONFIDENCE_THRESHOLD = 0.65


class ChatEngine:
    """Conversation engine with input validation, session handling, and error fallback."""

    def __init__(
        self,
        history: HistoryStore | None = None,
        interaction_log: InteractionLogStore | None = None,
        *,
        clear_file: bool = False,
    ):
        self._validator = InputValidator()
        self._classifier = IntentClassifier()
        self._responder = ResponseGenerator()
        self._history = history if history is not None else HistoryStore()
        self._interaction_log = interaction_log if interaction_log is not None else InteractionLogStore()
        self._session = ConversationSession()
        self._loaded_turns_count = 0

        self._load_recent_history_into_session()

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

            if clean.is_empty:
                intent = Intent.EMPTY
                effective_intent = Intent.EMPTY
                confidence = 1.0
            else:
                decision = self._classifier.classify_result(text)
                intent = decision.intent
                confidence = float(decision.confidence)
                effective_intent = intent

                try:
                    logger.info(
                        "Intent decision intent=%s confidence=%.3f candidates=%s",
                        getattr(decision.intent, "value", str(decision.intent)),
                        float(decision.confidence),
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
                    try:
                        candidates = self._classifier.classify_result(text).candidates
                    except Exception:
                        candidates = []

                    options = self._clarification_options_from_candidates(candidates)
                    response = self._responder.clarify(options)
                    effective_intent = "clarify"
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
            logger.exception("Error while processing turn error_type=%s", type(ex).__name__)
            fallback_used = True
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
            logger.exception("Error while classifying intent error_type=%s", type(ex).__name__)
            return Intent.UNKNOWN

    def route_intent(self, intent):
        """Return the handler function for a given intent."""
        if hasattr(intent, "value"):
            return self._responder.route_intent(intent)
        return self._responder.route_intent(Intent.UNKNOWN)

    def _load_recent_history_into_session(self) -> None:
        """Load saved history turns into the in memory session."""
        try:
            turns = self._history.load_turns()
        except Exception as ex:
            logger.warning("History load failed (non fatal): %s", ex)
            turns = []

        count = 0
        for turn in turns:
            try:
                self._session.add_message("user", turn.user_text)
                self._session.add_message("assistant", turn.assistant_text)
                count += 1
            except Exception:
                pass

        self._loaded_turns_count = count

    def _is_vague_unknown(self, text: str, intent: Intent) -> bool:
        if intent != Intent.UNKNOWN:
            return False

        t = (text or "").strip().casefold()
        if not t:
            return False

        vague = {
            "hi",
            "hello",
            "hey",
            "help",
            "h",
            "ok",
            "okay",
            "yo",
            "hmm",
            "huh",
            "what",
            "?",
        }
        return t in vague

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

        found.sort(key=lambda k: order.index(k) if k in order else 999)
        return found[:3]
