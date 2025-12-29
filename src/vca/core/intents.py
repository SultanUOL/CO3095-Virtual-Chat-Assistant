"""vca.core.intents

Intent detection for user input.

Rule based, deterministic classifier.

User story 22 priority policy
When multiple matches are found, choose the highest priority intent.

User story 23 confidence policy
Confidence is a deterministic float between 0 and 1 and is available via classify_result
and last_result. The classify method still returns Intent for backwards compatibility.
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
    intent: Intent
    rule: str
    candidates: List[Tuple[Intent, str]]


@dataclass(frozen=True)
class IntentResult:
    intent: Intent
    confidence: float
    rule: str
    candidates: List[Tuple[Intent, str]]


class IntentClassifier:
    _HELP_TOKENS = {"help", "h", "commands"}
    _HELP_PHRASES = {
        "what can you do",
        "what can u do",
        "what do you do",
        "what do u do",
        "show commands",
        "show help",
    }
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

    _COMMAND_INTENTS = {Intent.EXIT, Intent.HELP, Intent.HISTORY}

    def __init__(self) -> None:
        self.last_decision: IntentDecision | None = None
        self.last_result: IntentResult | None = None

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
            return phrase in lower
        return lower_no_edges == phrase or phrase in words

    def _base_confidence_for_rule(self, rule: str, intent: Intent) -> float:
        if intent == Intent.EMPTY:
            return 1.0
        if intent == Intent.UNKNOWN:
            return 0.2

        table = {
            "help_single_question_mark": 0.95,
            "help_token": 0.95,
            "help_phrase": 0.90,
            "exit_token": 0.95,
            "history_phrase": 0.90,
            "thanks_phrase": 0.90,
            "goodbye_phrase": 0.90,
            "greeting_phrase": 0.90,
            "question_mark": 0.85,
            "question_prefix": 0.75,
            "no_match": 0.20,
            "empty_input": 1.00,
        }
        return float(table.get(rule, 0.70))

    def _apply_ambiguity_penalty(self, base: float, selected: Intent, candidates: List[Tuple[Intent, str]]) -> float:
        distinct_intents = {i for i, _r in candidates}
        if len(distinct_intents) <= 1:
            return base

        has_command = any(i in self._COMMAND_INTENTS for i in distinct_intents)
        if has_command:
            return max(0.0, min(1.0, base - 0.35))

        return base

    def classify(self, raw_text: str | None) -> Intent:
        result = self.classify_result(raw_text)
        return result.intent

    def classify_result(self, raw_text: str | None) -> IntentResult:
        stripped, lower = self._normalize(raw_text)

        if stripped == "":
            decision = IntentDecision(Intent.EMPTY, "empty_input", [])
            self.last_decision = decision
            result = IntentResult(Intent.EMPTY, 1.0, decision.rule, decision.candidates)
            self.last_result = result
            return result

        lower_no_edges = self._strip_edge_punct(lower)
        words = set(self._words(lower))
        candidates: List[Tuple[Intent, str]] = []
        matched_help_phrase = False

        if lower == "?":
            candidates.append((Intent.HELP, "help_single_question_mark"))
        if lower_no_edges in self._HELP_TOKENS or any(w in self._HELP_TOKENS for w in words):
            candidates.append((Intent.HELP, "help_token"))

        for phrase in self._HELP_PHRASES:
            if self._phrase_matches(lower, lower_no_edges, words, phrase):
                candidates.append((Intent.HELP, "help_phrase"))
                matched_help_phrase = True
                break

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

        if not matched_help_phrase:
            if stripped.endswith("?"):
                candidates.append((Intent.QUESTION, "question_mark"))
            else:
                for prefix in self._QUESTION_PREFIXES:
                    if lower.startswith(prefix + " ") or lower == prefix:
                        candidates.append((Intent.QUESTION, "question_prefix"))
                        break

        if not candidates:
            decision = IntentDecision(Intent.UNKNOWN, "no_match", [])
            self.last_decision = decision
            result = IntentResult(Intent.UNKNOWN, 0.2, decision.rule, decision.candidates)
            self.last_result = result
            return result

        selected_intent, selected_rule = max(
            candidates,
            key=lambda item: self._PRIORITY.get(item[0], 0),
        )

        decision = IntentDecision(selected_intent, selected_rule, candidates)
        self.last_decision = decision

        base = self._base_confidence_for_rule(selected_rule, selected_intent)
        confidence = self._apply_ambiguity_penalty(base, selected_intent, candidates)
        confidence = max(0.0, min(1.0, float(confidence)))

        result = IntentResult(selected_intent, confidence, selected_rule, candidates)
        self.last_result = result
        return result