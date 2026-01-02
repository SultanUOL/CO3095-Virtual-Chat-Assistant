from __future__ import annotations
import re
import unicodedata

from dataclasses import dataclass

"""vca.core.validator

Centralised, deterministic input validation and normalisation.

This module is the single place where user input is cleaned before it reaches
intent classification and response generation.

User story 19 requires robust handling of edge cases:
1 Whitespace only input
2 Extremely long input with a defined truncation rule
3 Repeated punctuation and emoji without crashing
4 Control characters including tab and newline are normalised using a defined rule
"""


# All ASCII control characters (0x00-0x1F plus DEL). We will remove them after
# first normalising specific whitespace controls to spaces.
_CONTROL_CHARS = re.compile(r"[\x00-\x1F\x7F]")

# Any run of whitespace including spaces, tabs, newlines, and other unicode
# whitespace characters.
_WHITESPACE_RUN = re.compile(r"\s+")

# Collapse repeated punctuation deterministically. We allow up to 3 repeats.
_REPEAT_PUNCT = re.compile(r"([!?.,])\1{3,}")


@dataclass(frozen=True)
class CleanResult:
    text: str
    was_truncated: bool


class InputValidator:
    """Deterministic input cleaning rules used by ChatEngine.

    Rules (applied in order)
    1 Convert input to string (None becomes empty string)
    2 Unicode normalisation to NFC (keeps emoji, prevents odd combining forms)
    3 Normalise tabs and newlines to spaces
    4 Remove remaining ASCII control characters
    5 Collapse any whitespace runs to a single space and trim edges
    6 Collapse repeated punctuation sequences (!!!! -> !!!)
    7 Truncate extremely long input to a fixed max length

    These rules are predictable and safe for CLI usage.
    """

    MAX_LEN = 2000

    def clean(self, raw_text: object) -> CleanResult:
        # 1 Convert to string
        if raw_text is None:
            text = ""
        else:
            text = str(raw_text)

        # 2 Unicode normalisation (emoji safe)
        try:
            text = unicodedata.normalize("NFC", text)
        except Exception:
            pass

        # 3 Normalise common whitespace control chars to spaces
        text = (
            text.replace("\r\n", " ")
            .replace("\r", " ")
            .replace("\n", " ")
            .replace("\t", " ")
        )

        # 4 Remove remaining ASCII control characters
        text = _CONTROL_CHARS.sub("", text)

        # 5 Collapse whitespace and trim
        text = _WHITESPACE_RUN.sub(" ", text).strip()

        # 6 Collapse repeated punctuation deterministically
        while True:
            new_text = _REPEAT_PUNCT.sub(r"\1\1\1", text)
            if new_text == text:
                break
            text = new_text

        # 7 Truncate long input
        was_truncated = False
        if len(text) > self.MAX_LEN:
            text = text[: self.MAX_LEN]
            was_truncated = True

        return CleanResult(text=text, was_truncated=was_truncated)
