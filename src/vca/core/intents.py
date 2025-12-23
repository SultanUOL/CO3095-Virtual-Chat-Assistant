"""vca.core.intents

Intent detection for user input.

User story 22 priority policy

When multiple matches are found, choose the highest priority intent.

Priority order (highest first)
EXIT, HELP, HISTORY, THANKS, GOODBYE, GREETING, QUESTION, UNKNOWN
EMPTY is handled as a special case when input is blank.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class Intent(str, Enum):
    EMPTY = "empty"
    HELP = "help"
    EXIT = "exit"
    HISTORY = "history"
    GREETING = "greeting"
    QUESTION = "question"
    THANKS = "thanks"
    GOODBYE = "goodbye"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class IntentDecision:
    """Debug metadata about how a final intent was selected."""

    intent: Intent
    rule: str
    candidates: List[Tuple[Intent, str]]


class IntentClassifier:
    """Classifies user input into a small set of intents."""

    _HELP_TOKENS = {"help", "h", "commands"}
    _EXIT_TOKENS = {"exit", "quit", "q", "bye"}
    _HISTORY_PHRASES = {"history", "show history"}

    _THANKS_PHRASES = {"thanks", "thank you", "thx", "ty", "cheers"}
    _GOODBYE_PHRASES = {"goodbye", "good bye", "see you", "see ya", "later"}

    _GREETING_PHRASES = {
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

    _WORD_RE = re.compile(r"[a-z]+(?:'[a-z]+)?")

    # Higher number means higher priority
    _PRIORITY = {
        Intent.EXIT: 70,
        Intent.HELP: 60,
        Intent.HISTORY: 55,
        Intent.THANKS: 50,
        Intent.GOODBYE: 45,
        Intent.GREETING: 40,
        Intent.QUESTION: 30,
        Intent.UNKNOWN: 10,
    }

    def __init__(self) -> None:
        self.last_decision: IntentDecision | None = None

    @staticmethod
    def _normalize(raw_text: str | None) -> tuple[str, str]:
        text = "" if raw_text is None else str(raw_text)
        stripped = text.strip()
        lower = stripped.casefold()
        return stripped, lower

    @staticmethod
    def _strip_edge_punct(text: str) -> str:
        return text.strip(" \t\r\n!.,;:()[]{}\"'")

    def _words(self, lower: str) -> List[str]:
        return self._WORD_RE.findall(lower)

    def _phrase_matches(self, lower: str, lower_no_edges: str, words: set[str], phrase: str) -> bool:
        phrase = phrase.casefold()
        if " " in phrase:
            # Multi word phrase match, safe to use substring because it includes spaces
            return phrase in lower
        # Single word phrase match must be a whole word, not a substring inside another word
        return lower_no_edges == phrase or phrase in words

    def classify(self, raw_text: str | None) -> Intent:
        stripped, lower = self._normalize(raw_text)

        if stripped == "":
            self.last_decision = IntentDecision(Intent.EMPTY, "empty_input", [])
            return Intent.EMPTY

        lower_no_edges = self._strip_edge_punct(lower)
        words = set(self._words(lower))

        candidates: List[Tuple[Intent, str]] = []

        # HELP: keep legacy behaviour where a single "?" is help
        if lower == "?":
            candidates.append((Intent.HELP, "help_single_question_mark"))
        if lower_no_edges in self._HELP_TOKENS or any(w in self._HELP_TOKENS for w in words):
            candidates.append((Intent.HELP, "help_token"))

        if lower_no_edges in self._EXIT_TOKENS or any(w in self._EXIT_TOKENS for w in words):
            candidates.append((Intent.EXIT, "exit_token"))

        for phrase in self._HISTORY_PHRASES:
            if self._phrase_matches(lower, lower_no_edges, words, phrase):
                candidates.append((Intent.HISTORY, "history_phrase"))
                break

        for phrase in self._THANKS_PHRASES:
            if self._phrase_matches(lower, lower_no_edges, words, phrase):
                candidates.append((Intent.THANKS, "thanks_phrase"))
                break

        for phrase in self._GOODBYE_PHRASES:
            if self._phrase_matches(lower, lower_no_edges, words, phrase):
                candidates.append((Intent.GOODBYE, "goodbye_phrase"))
                break

        for phrase in self._GREETING_PHRASES:
            if self._phrase_matches(lower, lower_no_edges, words, phrase):
                candidates.append((Intent.GREETING, "greeting_phrase"))
                break

        # Question rule can overlap with other rules, priority resolves it
        if stripped.endswith("?"):
            candidates.append((Intent.QUESTION, "question_mark"))
        else:
            for prefix in self._QUESTION_PREFIXES:
                if lower.startswith(prefix + " ") or lower == prefix:
                    candidates.append((Intent.QUESTION, "question_prefix"))
                    break

        if not candidates:
            self.last_decision = IntentDecision(Intent.UNKNOWN, "no_match", [])
            return Intent.UNKNOWN

        selected_intent, selected_rule = max(
            candidates,
            key=lambda item: self._PRIORITY.get(item[0], 0),
        )

        self.last_decision = IntentDecision(
            intent=selected_intent,
            rule=selected_rule,
            candidates=candidates,
        )
        return selected_intent