"""vca.core.engine

Core conversation engine.

Coordinates validation, intent classification, response generation, and session
persistence.
"""

from __future__ import annotations

from dataclasses import dataclass
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

# Bounded in memory retention of session content to avoid unbounded growth.
# This is a best effort bound because ConversationSession is owned elsewhere.
_SESSION_MAX_TURNS = 200


@dataclass(frozen=True)
class _ValidatedInput:
    """Represents the validated and cleaned user input for a single turn."""

    text: str
    input_length: int
    was_truncated: bool


@dataclass
class _TurnTelemetry:
    """Telemetry that we record for each processed turn."""

    rule_match_count: int = 0
    multiple_rules_matched: bool = False
    input_length: int = 0
    effective_intent: Intent | str = Intent.UNKNOWN
    confidence: float = 0.0
    fallback_used: bool = False
    started: float = 0.0


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
                self._enforce_bounded_session()
            except Exception as ex:
                logger.warning("History load failed non fatal error_type=%s", type(ex).__name__)
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

    def _enforce_bounded_session(self) -> None:
        """
        Best effort enforcement of bounded in memory history.

        Strategy
        Use a trim method if available.
        Otherwise attempt to trim common private attributes by convention.
        Never raises.
        """
        try:
            trim_turns = getattr(self._session, "trim_to_last_turns", None)
            if callable(trim_turns):
                trim_turns(_SESSION_MAX_TURNS)
                return
        except Exception:
            pass

        try:
            trim_msgs = getattr(self._session, "trim_to_last_messages", None)
            if callable(trim_msgs):
                trim_msgs(_SESSION_MAX_TURNS * 2)
                return
        except Exception:
            pass

        try:
            for attr in ("_turns", "_messages", "turns", "messages"):
                buf = getattr(self._session, attr, None)
                if isinstance(buf, list):
                    limit = _SESSION_MAX_TURNS * 2
                    if len(buf) > limit:
                        setattr(self._session, attr, buf[-limit:])
                        return
        except Exception:
            pass

    def _stage_validate(self, raw_text: str | None) -> _ValidatedInput:
        """Validate and normalize raw user input."""
        clean = self._validator.clean(raw_text)
        text = clean.text
        return _ValidatedInput(text=text, input_length=len(text), was_truncated=clean.was_truncated)

    def _stage_load_context(self):
        """Fetch the recent session turns used as the context window."""
        return self._session.recent_turns(limit=CONTEXT_WINDOW_TURNS)

    def _stage_handle_pending_clarification(
        self,
        validated: _ValidatedInput,
        context_turns,
        telemetry: _TurnTelemetry,
    ) -> str | None:
        """Handle a follow up answer when we previously asked a clarifying question."""
        if self._session.pending_clarification is None:
            return None

        state = self._session.pending_clarification
        text = validated.text
        choice = self._parse_clarification_choice(text, state.options)

        self._session.add_message("user", text)
        self._enforce_bounded_session()
        recent = self._session.recent_messages(limit=10)

        if choice is None:
            self._session.clear_pending_clarification()
            telemetry.effective_intent = Intent.UNKNOWN
            handler = self.route_intent(Intent.UNKNOWN)
            response = self._invoke_handler(handler, text, recent, context_turns)
        else:
            self._session.clear_pending_clarification()
            telemetry.effective_intent = choice
            handler = self.route_intent(choice)
            response = self._invoke_handler(handler, state.original_text, recent, context_turns)

        response = self._stage_apply_truncation_note(response, validated.was_truncated)

        self._session.add_message("assistant", response)
        self._enforce_bounded_session()
        self._safe_save_history(text, response, telemetry.effective_intent)
        return response

    def _stage_classify_intent(self, text: str, telemetry: _TurnTelemetry) -> tuple[Intent, object | None]:
        """Classify intent for the input."""
        intent = self._classifier.classify(text)
        result = getattr(self._classifier, "last_result", None)
        candidates = getattr(result, "candidates", None) if result is not None else None
        telemetry.rule_match_count = len(candidates or [])
        telemetry.multiple_rules_matched = telemetry.rule_match_count > 1
        telemetry.effective_intent = intent

        if result is not None:
            try:
                telemetry.confidence = float(result.confidence)
            except Exception:
                telemetry.confidence = 0.0

        return intent, result

    def _stage_add_user_message(self, text: str):
        """Append the user message to the session and return recent messages."""
        self._session.add_message("user", text)
        self._enforce_bounded_session()
        return self._session.recent_messages(limit=10)

    def _stage_maybe_ask_for_clarification(
        self,
        text: str,
        intent: Intent,
        classifier_result: object | None,
        telemetry: _TurnTelemetry,
    ) -> str | None:
        """Decide if we should ask the user a clarifying question."""
        if self._looks_like_multi_intent(text):
            telemetry.fallback_used = True
            options = ["exit", "help"]
            self._session.set_pending_clarification(original_text=text, options=options)
            response = self._responder.generate_clarifying_question(options)
            self._session.add_message("assistant", response)
            self._enforce_bounded_session()
            self._safe_save_history(text, response, "clarify")
            return response

        confidence = telemetry.confidence
        if confidence and confidence < CONFIDENCE_THRESHOLD and intent not in (Intent.EMPTY, Intent.UNKNOWN):
            telemetry.fallback_used = True
            candidates = getattr(classifier_result, "candidates", []) if classifier_result is not None else []
            options = self._clarification_options_from_candidates(candidates)
            self._session.set_pending_clarification(original_text=text, options=options)
            response = self._responder.generate_clarifying_question(options)
            self._session.add_message("assistant", response)
            self._enforce_bounded_session()
            self._safe_save_history(text, response, "clarify")
            return response

        return None

    def _stage_generate_response(self, text: str, intent: Intent, recent, context_turns) -> str:
        """Generate the assistant response for the current turn."""
        faq = self._responder.faq_response_for(text)
        if faq is not None:
            return faq

        handler = self.route_intent(intent)
        return self._invoke_handler(handler, text, recent, context_turns)

    def _stage_apply_truncation_note(self, response: str, was_truncated: bool) -> str:
        """Append the input truncated note when the validator truncated the input."""
        if was_truncated:
            return response + "  Note: your input was truncated."
        return response

    def _stage_persist_and_return(self, user_text: str, response: str, intent, telemetry: _TurnTelemetry) -> str:
        """Persist the completed turn and return the response."""
        self._session.add_message("assistant", response)
        self._enforce_bounded_session()
        self._safe_save_history(user_text, response, intent)
        telemetry.effective_intent = intent
        return response

    def _stage_log_telemetry(self, telemetry: _TurnTelemetry) -> None:
        """Log interaction telemetry for the turn."""
        try:
            elapsed_ms = int((time.perf_counter() - telemetry.started) * 1000)
            self._interaction_log.append_event(
                input_length=telemetry.input_length,
                intent=telemetry.effective_intent,
                fallback_used=telemetry.fallback_used,
                confidence=telemetry.confidence,
                processing_time_ms=elapsed_ms,
                rule_match_count=telemetry.rule_match_count,
                multiple_rules_matched=telemetry.multiple_rules_matched,
            )
        except Exception:
            pass

    def process_turn(self, raw_text: str | None) -> str:
        telemetry = _TurnTelemetry(started=time.perf_counter())

        try:
            validated = self._stage_validate(raw_text)
            telemetry.input_length = validated.input_length

            context_turns = self._stage_load_context()

            pending_response = self._stage_handle_pending_clarification(validated, context_turns, telemetry)
            if pending_response is not None:
                return pending_response

            try:
                intent, result = self._stage_classify_intent(validated.text, telemetry)
            except Exception as ex:
                telemetry.fallback_used = True
                telemetry.effective_intent = Intent.UNKNOWN
                try:
                    error_logger.exception(
                        "Error while classifying intent error_type=%s intent=%s file_operation=False",
                        type(ex).__name__,
                        str(telemetry.effective_intent),
                    )
                except Exception:
                    pass
                return self._responder.fallback_error()

            recent = self._stage_add_user_message(validated.text)

            clarification = self._stage_maybe_ask_for_clarification(validated.text, intent, result, telemetry)
            if clarification is not None:
                return clarification

            try:
                response = self._stage_generate_response(validated.text, intent, recent, context_turns)
            except Exception as ex:
                telemetry.fallback_used = True
                telemetry.effective_intent = Intent.UNKNOWN
                try:
                    error_logger.exception(
                        "Error while generating response error_type=%s intent=%s file_operation=False",
                        type(ex).__name__,
                        str(telemetry.effective_intent),
                    )
                except Exception:
                    pass
                response = self._responder.fallback_error()

            response = self._stage_apply_truncation_note(response, validated.was_truncated)

            try:
                return self._stage_persist_and_return(validated.text, response, telemetry.effective_intent, telemetry)
            except Exception as ex:
                telemetry.fallback_used = True
                telemetry.effective_intent = Intent.UNKNOWN
                try:
                    error_logger.exception(
                        "Error while persisting response error_type=%s intent=%s file_operation=True",
                        type(ex).__name__,
                        str(telemetry.effective_intent),
                    )
                except Exception:
                    pass
                return self._responder.fallback_error()

        except Exception as ex:
            telemetry.fallback_used = True
            telemetry.effective_intent = Intent.UNKNOWN
            try:
                error_logger.exception(
                    "Error while processing turn error_type=%s intent=%s file_operation=False",
                    type(ex).__name__,
                    str(telemetry.effective_intent),
                )
            except Exception:
                pass

            fallback = self._responder.fallback_error()
            try:
                self._session.add_message("assistant", fallback)
                self._enforce_bounded_session()
            except Exception:
                pass
            return fallback

        finally:
            self._stage_log_telemetry(telemetry)

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
