"""vca.core.intents

Intent detection for user input.

This module is intentionally rule based to keep behaviour deterministic and easy to
unit test. It is also intentionally separate from response generation so that intent
rules can evolve without changing reply text.
"""

from __future__ import annotations

from enum import Enum


class Intent(str, Enum):
    """Supported intents for the assistant.

    Values are strings so they are easy to log, serialize, and compare in tests.
    """

    EMPTY = "empty"
    HELP = "help"
    EXIT = "exit"
    HISTORY = "history"
    GREETING = "greeting"
    QUESTION = "question"
    THANKS = "thanks"
    GOODBYE = "goodbye"
    UNKNOWN = "unknown"


class IntentClassifier:
    """Classifies user input into a small set of intents.

    Design goals
    Deterministic: same input always yields the same output
    Simple: small rule set that is easy to reason about and test
    """

    _HELP_TOKENS = {"help", "h", "?", "commands"}
    _EXIT_TOKENS = {"exit", "quit", "q"}
    _HISTORY_TOKENS = {"history", "show history"}

    _THANKS_TOKENS = {"thanks", "thank you", "thx", "ty", "cheers"}
    _GOODBYE_TOKENS = {"goodbye", "good bye", "see you", "see ya", "later"}

    _GREETING_TOKENS = {
        "hi",
        "hello",
        "hey",
        "yo",
        "good morning",
        "good afternoon",
        "good evening",
    }

    _QUESTION_PREFIXES = (
        "what",
        "why",
        "how",
        "when",
        "where",
        "who",
        "which",
        "can you",
        "could you",
        "do you",
        "does",
        "is",
        "are",
        "should",
        "would",
        "will",
    )

    @staticmethod
    def _normalize(raw_text: str | None) -> tuple[str, str]:
        """Return (stripped, lower) forms for consistent rule checks."""
        text = "" if raw_text is None else str(raw_text)
        stripped = text.strip()
        lower = stripped.casefold()
        return stripped, lower

    def classify(self, raw_text: str | None) -> Intent:
        """Return the intent for the provided text."""
        stripped, lower = self._normalize(raw_text)

        if stripped == "":
            return Intent.EMPTY

        if lower in self._HELP_TOKENS:
            return Intent.HELP

        if lower in self._EXIT_TOKENS:
            return Intent.EXIT

        if lower in self._HISTORY_TOKENS:
            return Intent.HISTORY

        if lower in self._THANKS_TOKENS:
            return Intent.THANKS

        if lower in self._GOODBYE_TOKENS:
            return Intent.GOODBYE

        if lower in self._GREETING_TOKENS:
            return Intent.GREETING

        if stripped.endswith("?"):
            return Intent.QUESTION

        for prefix in self._QUESTION_PREFIXES:
            if lower == prefix or lower.startswith(prefix + " "):
                return Intent.QUESTION

        return Intent.UNKNOWN