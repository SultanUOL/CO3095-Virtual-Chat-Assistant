from __future__ import annotations

import re
from dataclasses import dataclass


_CONTROL_CHARS_EXCEPT_TAB_NEWLINE = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")


@dataclass(frozen=True)
class CleanResult:
    text: str
    was_truncated: bool


class InputValidator:
    """
    Deterministic input cleaning rules.

    Rules
    1 Always convert input to string
    2 Remove leading and trailing whitespace
    3 Remove control characters except tab and newline
    4 Truncate extremely long input to a fixed max length

    These rules are designed to be predictable and safe for CLI usage.
    """

    MAX_LEN = 2000

    def clean(self, raw_text: object) -> CleanResult:
        if raw_text is None:
            text = ""
        else:
            text = str(raw_text)

        text = _CONTROL_CHARS_EXCEPT_TAB_NEWLINE.sub("", text)

        text = text.strip()

        was_truncated = False
        if len(text) > self.MAX_LEN:
            text = text[: self.MAX_LEN]
            was_truncated = True

        return CleanResult(text=text, was_truncated=was_truncated)
