"""
Core conversation engine.
Coordinates parsing, intent classification, response generation, and persistence.
"""

from vca.core.intents import IntentClassifier
from vca.core.responses import ResponseGenerator
from vca.storage.history_store import HistoryStore


class ChatEngine:
    """
    High level orchestrator.

    This class will intentionally contain branching later to support coverage,
    symbolic execution, and concolic testing requirements.
    """

    def __init__(self) -> None:
        self._classifier = IntentClassifier()
        self._responder = ResponseGenerator()
        self._history = HistoryStore()

    def process_turn(self, raw_text: str) -> str:
        if raw_text is None:
            text = ""
        else:
            text = str(raw_text)

        intent = self._classifier.classify(text)
        response = self._responder.generate(intent, text)
        return response

    def classify_intent(self, raw_text: str) -> str:
        if raw_text is None:
            text = ""
        else:
            text = str(raw_text)
        return self._classifier.classify(text)
