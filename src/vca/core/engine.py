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
        """
        Process one user input and return one assistant reply.

        Sprint 1 will implement input validation and basic intents.
        """
        raise NotImplementedError("Sprint 1 will implement process_turn.")
