"""
Helper classes for testing.
These are used across multiple test files.
"""

from typing import List
from vca.domain.chat_turn import ChatTurn
from vca.storage.history_store import HistoryStore
from vca.storage.interaction_log_store import InteractionLogStore
from vca.core.engine import ChatEngine


class FakeHistory(HistoryStore):
    """In-memory fake history store for testing."""

    def __init__(self):
        self.turns: List[ChatTurn] = []
        self.saved: List[
            tuple[str, str]
        ] = []  # List of (user_text, assistant_text) tuples
        # Initialize with a dummy path - we override all file operations
        super().__init__(path=None)  # type: ignore

    def save_turn(self, user_text: str, assistant_text: str) -> None:

        turn = ChatTurn(user_text=user_text, assistant_text=assistant_text)
        self.turns.append(turn)
        self.saved.append((user_text, assistant_text))

    def load_turns(self, max_turns: int | None = None) -> List[ChatTurn]:
        turns = self.turns.copy()
        if max_turns is not None:
            turns = turns[-max_turns:]
        return turns

    def clear_file(self) -> None:
        self.turns.clear()
        self.saved.clear()

    def flush(self) -> None:
        return

    def close(self) -> None:
        return


class FakeInteractionLog(InteractionLogStore):
    """In-memory fake interaction log for testing."""

    def __init__(self):
        self.events: List[dict] = []
        # Initialize with a dummy path - we override all file operations
        super().__init__(path=None)  # type: ignore

    def append_event(
        self,
        input_length: int,
        intent: str,
        fallback_used: bool,
        confidence: float = 0.0,
        processing_time_ms: int = 0,
        rule_match_count: int = 0,
        multiple_rules_matched: bool = False,
    ) -> None:
        from datetime import datetime

        event = {
            "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "input_length": input_length,
            "intent": str(intent),
            "confidence": confidence,
            "fallback_used": fallback_used,
            "processing_time_ms": processing_time_ms,
            "rule_match_count": rule_match_count,
            "multiple_rules_matched": multiple_rules_matched,
        }
        self.events.append(event)

    def flush(self) -> None:
        return

    def close(self) -> None:
        return


class SeqClock:
    """Sequential clock that returns predefined values for deterministic testing."""

    def __init__(self, values: List[float]):
        self.values = values
        self.index = 0

    def __call__(self) -> float:
        if self.index < len(self.values):
            val = self.values[self.index]
            self.index += 1
            return val
        return self.values[-1] if self.values else 0.0


class _FakeEngine(ChatEngine):
    """Fake engine for testing CLI without real processing."""

    def __init__(self):
        super().__init__()
        self.calls: List[str] = []
        self.seen: List[str] = []  # Tracks actual messages (not commands)
        self.cleared = False
        self.reset_calls = 0

    def process_turn(self, text: str) -> str:
        self.calls.append(text)
        # Track actual messages (not empty/help/exit commands)
        if text and text.strip().lower() not in ["help", "exit", "restart", "reset"]:
            self.seen.append(text)
        if text.strip().lower() == "exit":
            return "Goodbye!"
        # Return format that matches test expectation
        return f"reply: {text}"

    def clear_history(self, clear_file: bool = True) -> None:
        """Clear history (called on exit)."""
        super().clear_history(clear_file=clear_file)
        self.cleared = True

    def reset_session(self) -> None:
        """Reset the session (called by CLI restart command)."""
        super().reset_session()
        self.reset_calls += 1
        self.cleared = True
        self.seen.clear()  # Clear seen messages on restart
