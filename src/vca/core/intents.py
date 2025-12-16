"""
Intent detection for user input.
Rule based to keep behavior deterministic and testable.
"""


class IntentClassifier:
    """Classifies user input into a small set of intents."""

    def classify(self, raw_text: str) -> str:
        """
        Return an intent label such as help, exit, history, unknown.

        Sprint 1 will implement branching and validation logic here.
        """
        raise NotImplementedError("Sprint 1 will implement classify.")
