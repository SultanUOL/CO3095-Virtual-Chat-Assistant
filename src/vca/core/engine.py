# src/vca/core/engine.py
"""vca.core.engine

Core conversation engine.

Coordinates validation, intent classification, response generation, and session
persistence.
"""

from __future__ import annotations

import logging
import re
import time

from vca.core.intents import Intent, IntentClassifier
from vca.core.responses import ResponseGenerator
from vca.core.validator import InputValidator
from vca.domain.constants import CONTEXT_WINDOW_TURNS
from vca.domain.session import ConversationSession
from vca.storage.history_store import HistoryStore
from vca.storage.interaction_log_store import InteractionLogStore

logger = logging.getLogger(__name__)
error_logger = logging.getLogger("vca.errors")

CONFIDENCE_THRESHOLD = 0.65


class ChatEngine:
    _WORD_RE = re.compile(r"[a-z]+(?:'[a-z]+)?")

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

    @property
    def session(self) -> ConversationSession:
        return self._session

    @property
    def loaded_turns_count(self) -> int:
        return self._loaded_turns_count

    def reset_session(self) -> None:
        try:
            self._session.clear()
        except Exception:
            pass

    def clear_history(self, clear_file: bool = True) -> None:
        self.reset_session()
        if clear_file:
            try:
                self._history.clear_file()
            except Exception:
                pass

    def shutdown(self) -> None:
        try:
            flush = getattr(self._history, "flush", None)
            if callable(flush):
                flush()
        except Exception:
            pass

        try:
            flush = getattr(self._interaction_log, "flush", None)
            if callable(flush):
                flush()
        except Exception:
            pass

        try:
            close = getattr(self._history, "close", None)
            if callable(close):
                close()
        except Exception:
            pass

        try:
            close = getattr(self._interaction_log, "close", None)
            if callable(close):
                close()
        except Exception:
            pass

        try:
            logging.shutdown()
        except Exception:
            pass

    def classify_intent(self, text: str) -> Intent:
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
                pass
            return Intent.UNKNOWN

    def route_intent(self, intent):
        """
        Required for older tests.
        Returns a specific ResponseGenerator handler for a given intent string or enum.
        """
        if intent is None:
            return self._responder.route("unknown")

        if hasattr(intent, "value"):
            return self._responder.route(str(intent.value))

        return self._responder.route(str(intent))

    def _invoke_handler(self, handler, text: str, recent, context_turns):
        """
        Some tests monkeypatch a handler that only accepts 2 parameters.
        We attempt 3 first, then fallback to 2.
        """
        try:
            return handler(text, recent, context_turns)
        except TypeError:
            return handler(text, recent)

    def process_turn(self, raw_text: str | None) -> str:
        rule_match_count = 0
        multiple_rules_matched = False
        input_length = 0
        effective_intent: Intent | str = Intent.UNKNOWN
        confidence = 0.0
        fallback_used = False
        started = time.perf_counter()

        try:
            clean = self._validator.clean(raw_text)
            text = clean.text
            input_length = len(text)

            context_turns = self._session.recent_turns(limit=CONTEXT_WINDOW_TURNS)

            if self._session.pending_clarification is not None:
                state = self._session.pending_clarification
                choice = self._parse_clarification_choice(text, state.options)

                self._session.add_message("user", text)
                recent = self._session.recent_messages(limit=10)

                if choice is None:
                    self._session.clear_pending_clarification()
                    effective_intent = Intent.UNKNOWN
                    handler = self.route_intent(Intent.UNKNOWN)
                    response = self._invoke_handler(handler, text, recent, context_turns)
                else:
                    self._session.clear_pending_clarification()
                    effective_intent = choice
                    handler = self.route_intent(choice)
                    response = self._invoke_handler(handler, state.original_text, recent, context_turns)

                if clean.was_truncated:
                    response = response + "  Note: your input was truncated."

                self._session.add_message("assistant", response)
                self._safe_save_history(text, response, effective_intent)
                return response

            try:
                intent = self._classifier.classify(text)
                result = getattr(self._classifier, "last_result", None)
                candidates = getattr(result, "candidates", None) if result is not None else None
                rule_match_count = len(candidates or [])
                multiple_rules_matched = rule_match_count > 1
            except Exception as ex:
                fallback_used = True
                effective_intent = Intent.UNKNOWN
                try:
                    error_logger.exception(
                        "Error while classifying intent error_type=%s intent=%s file_operation=False",
                        type(ex).__name__,
                        str(effective_intent),
                    )
                except Exception:
                    pass
                return self._responder.fallback_error()

            effective_intent = intent

            result = getattr(self._classifier, "last_result", None)
            if result is not None:
                try:
                    confidence = float(result.confidence)
                except Exception:
                    confidence = 0.0

            self._session.add_message("user", text)
            recent = self._session.recent_messages(limit=10)

            if self._looks_like_multi_intent(text):
                fallback_used = True
                options = ["exit", "help"]
                self._session.set_pending_clarification(original_text=text, options=options)
                response = self._responder.generate_clarifying_question(options)
                self._session.add_message("assistant", response)
                self._safe_save_history(text, response, "clarify")
                return response

            if confidence and confidence < CONFIDENCE_THRESHOLD and intent not in (Intent.EMPTY, Intent.UNKNOWN):
                fallback_used = True
                options = self._clarification_options_from_candidates(getattr(result, "candidates", []) if result else [])
                self._session.set_pending_clarification(original_text=text, options=options)
                response = self._responder.generate_clarifying_question(options)
                self._session.add_message("assistant", response)
                self._safe_save_history(text, response, "clarify")
                return response

            faq = self._responder.faq_response_for(text)
            if faq is not None:
                response = faq
            else:
                handler = self.route_intent(intent)
                response = self._invoke_handler(handler, text, recent, context_turns)

            if clean.was_truncated:
                response = response + "  Note: your input was truncated."

            self._session.add_message("assistant", response)
            self._safe_save_history(text, response, effective_intent)
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
                pass

            fallback = self._responder.fallback_error()
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
                    rule_match_count=rule_match_count,
                    multiple_rules_matched=multiple_rules_matched,
                )
            except Exception:
                pass

    def _safe_save_history(self, user_text: str, assistant_text: str, intent) -> None:
        try:
            self._history.save_turn(user_text, assistant_text)
        except Exception as ex:
            try:
                error_logger.exception(
                    "History save failed error_type=%s intent=%s file_operation=True",
                    type(ex).__name__,
                    str(intent),
                )
            except Exception:
                pass

    def _looks_like_multi_intent(self, text: str) -> bool:
        t = (text or "").strip().casefold()
        if t == "":
            return False

        tokens = set(self._WORD_RE.findall(t))

        help_tokens = {"help", "h", "commands"}
        exit_tokens = {"exit", "quit", "q", "bye", "goodbye"}

        has_help = any(tok in help_tokens for tok in tokens)
        has_exit = any(tok in exit_tokens for tok in tokens)

        return has_help and has_exit

    def _clarification_options_from_candidates(self, candidates) -> list[str]:
        order = ["exit", "help", "history", "thanks", "goodbye", "greeting", "question"]
        seen: set[str] = set()
        found: list[str] = []

        for item in candidates or []:
            cand_intent = item[0]
            value = cand_intent.value if hasattr(cand_intent, "value") else str(cand_intent)
            key = str(value).strip().casefold()
            if key in {"unknown", "empty"}:
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