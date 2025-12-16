"""
File based storage for chat history.
No database. Uses simple serialization in later sprints.
"""

from typing import List


class HistoryStore:
    """Stores and loads chat history from disk."""

    def save_turn(self, user_text: str, assistant_text: str) -> None:
        """Persist one conversation turn."""
        raise NotImplementedError("Sprint 1 will implement save_turn.")

    def load_history(self) -> List[str]:
        """Load prior history in a display friendly form."""
        raise NotImplementedError("Sprint 1 will implement load_history.")
