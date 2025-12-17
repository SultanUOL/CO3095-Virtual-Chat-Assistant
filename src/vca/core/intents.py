"""
Intent detection for user input.
Rule based to keep behavior deterministic and testable.
"""


class IntentClassifier:
    """Classifies user input into a small set of intents."""

    def classify(self, raw_text: str) -> str:
        if raw_text is None:
            text = ""
        else:
            text = str(raw_text)

        stripped = text.strip()
        if stripped == "":
            return "empty"

        lower = stripped.casefold()

        if lower in {"help", "h", "?", "commands"}:
            return "help"

        if lower in {"exit", "quit", "q", "bye"}:
            return "exit"

        if lower in {"history", "show history"}:
            return "history"

        return "unknown"
