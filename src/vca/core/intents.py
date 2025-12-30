"""vca.core.intents

Intent detection for user input.

Rule based, deterministic classifier.

User story 22 priority policy
When multiple matches are found, choose the highest priority intent.

User story 23 confidence policy
Confidence is a deterministic float between 0 and 1 and is available via classify_result
and last_result. The classify method still returns Intent for backwards compatibility.

User story 38 synonym policy
Synonyms are defined in one place and matched case insensitively after trimming
leading and trailing whitespace.

User story 39 false positive policy
Matching avoids partial substring triggers by using token boundaries and phrase
matching on word sequences. Exact command inputs for help and exit are preferred.

User story 35 performance policy
Regex patterns and phrase tokenization are precomputed so classify_result avoids
repeated compilation and repeated phrase splitting.
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
    """
    Synonym groups

    This dictionary is the single source of truth for synonym based intent matching.
    Each intent maps to one or more groups.

    Each group is a tuple:
    match_type, values, rule_label

    match_type "token" matches individual words only.
    match_type "phrase" matches word sequences, not raw substrings.
    """

    _SYNONYM_GROUPS: dict[Intent, list[tuple[str, set[str], str]]] = {
        Intent.HELP: [
            ("token", {"help", "h", "commands"}, "help_token"),
            (
                "phrase",
                {
                    "what can you do",
                    "what can u do",
                    "what do you do",
                    "what do u do",
                    "show commands",
                    "show help",
                },
                "help_phrase",
            ),
        ],
        Intent.EXIT: [
            ("token", {"exit", "quit", "q", "bye"}, "exit_token"),
        ],
        Intent.HISTORY: [
            ("phrase", {"history", "show history"}, "history_phrase"),
        ],
        Intent.THANKS: [
            ("phrase", {"thanks", "thank you", "thx", "ty", "cheers"}, "thanks_phrase"),
        ],
        Intent.GOODBYE: [
            ("phrase", {"goodbye", "good bye", "see you", "see ya", "later"}, "goodbye_phrase"),
        ],
        Intent.GREETING: [
            (
                "phrase",
                {"hi", "hello", "hey", "yo", "good morning", "good afternoon", "good evening"},
                "greeting_phrase",
            ),
        ],
    }

    # Compatibility alias so older code and tests do not crash.
    _SYNONYM_REPHRASE_GROUPS = _SYNONYM_GROUPS

    _HELP_COMMAND_TOKENS = {"help", "h", "commands"}
    _EXIT_COMMAND_TOKENS = {"exit", "quit", "q", "bye"}

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

    # Priority ordering, higher wins.
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

    # Precompiled phrase tokens for performance.
    # Structure:
    # intent -> list of groups
    # group for token: ("token", set[str], rule)
    # group for phrase: ("phrase", list[list[str]], rule)
    _COMPILED_GROUPS: dict[Intent, list[tuple[str, object, str]]] = {}

    @classmethod
    def _compile_groups(cls) -> dict[Intent, list[tuple[str, object, str]]]:
        compiled: dict[Intent, list[tuple[str, object, str]]] = {}
        for intent, groups in cls._SYNONYM_GROUPS.items():
            out_groups: list[tuple[str, object, str]] = []
            for match_type, values, rule in groups:
                if match_type == "token":
                    out_groups.append((match_type, values, rule))
                else:
                    phrase_words_list: list[list[str]] = []
                    for phrase in values:
                        phrase_lower = phrase.casefold()
                        words = cls._WORD_RE.findall(phrase_lower)
                        phrase_words_list.append(words)
                    out_groups.append((match_type, phrase_words_list, rule))
            compiled[intent] = out_groups
        return compiled

    def __init__(self) -> None:
        self.last_decision: IntentDecision | None = None
        self.last_result: IntentResult | None = None

        if not self._COMPILED_GROUPS:
            IntentClassifier._COMPILED_GROUPS = self._compile_groups()

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

    @staticmethod
    def _is_exact_command(lower_no_edges: str, word_list: List[str], command_tokens: set[str]) -> bool:
        if len(word_list) != 1:
            return False
        if word_list[0] != lower_no_edges:
            return False
        return lower_no_edges in command_tokens

    @staticmethod
    def _phrase_words_match(word_list: List[str], phrase_words: List[str]) -> bool:
        if not phrase_words:
            return False
        if len(phrase_words) == 1:
            return phrase_words[0] in word_list
        if len(word_list) < len(phrase_words):
            return False

        last = len(word_list) - len(phrase_words)
        for i in range(0, last + 1):
            if word_list[i : i + len(phrase_words)] == phrase_words:
                return True
        return False

    def _base_confidence_for_rule(self, rule: str, intent: Intent) -> float:
        if intent == Intent.EMPTY:
            return 1.0
        if intent == Intent.UNKNOWN:
            return 0.2

        table = {
            "help_single_question_mark": 0.95,
            "help_exact": 0.98,
            "help_token": 0.95,
            "help_phrase": 0.90,
            "exit_exact": 0.98,
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
        word_list = self._words(lower)
        words_set = set(word_list)

        candidates: List[Tuple[Intent, str]] = []
        matched_help_phrase = False

        is_help_exact = self._is_exact_command(lower_no_edges, word_list, self._HELP_COMMAND_TOKENS)
        is_exit_exact = self._is_exact_command(lower_no_edges, word_list, self._EXIT_COMMAND_TOKENS)

        if lower == "?":
            candidates.append((Intent.HELP, "help_single_question_mark"))

        if is_help_exact:
            candidates.append((Intent.HELP, "help_exact"))

        if is_exit_exact:
            candidates.append((Intent.EXIT, "exit_exact"))

        for intent, groups in self._COMPILED_GROUPS.items():
            for match_type, values_obj, rule in groups:
                if intent == Intent.HELP and is_help_exact and rule == "help_token":
                    continue
                if intent == Intent.EXIT and is_exit_exact and rule == "exit_token":
                    continue

                if match_type == "token":
                    values = values_obj  # type: ignore[assignment]
                    if lower_no_edges in values or any(w in values for w in words_set):
                        candidates.append((intent, rule))
                else:
                    phrase_words_list = values_obj  # type: ignore[assignment]
                    for phrase_words in phrase_words_list:
                        if not phrase_words:
                            continue
                        if len(phrase_words) == 1:
                            if phrase_words[0] == lower_no_edges or phrase_words[0] in words_set:
                                candidates.append((intent, rule))
                                if intent == Intent.HELP and rule == "help_phrase":
                                    matched_help_phrase = True
                                break
                        else:
                            if self._phrase_words_match(word_list, phrase_words):
                                candidates.append((intent, rule))
                                if intent == Intent.HELP and rule == "help_phrase":
                                    matched_help_phrase = True
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

        selected_intent, selected_rule = max(candidates, key=lambda item: self._PRIORITY.get(item[0], 0))

        decision = IntentDecision(selected_intent, selected_rule, candidates)
        self.last_decision = decision

        base = self._base_confidence_for_rule(selected_rule, selected_intent)
        confidence = self._apply_ambiguity_penalty(base, selected_intent, candidates)
        confidence = max(0.0, min(1.0, float(confidence)))

        result = IntentResult(selected_intent, confidence, selected_rule, candidates)
        self.last_result = result
        return result
