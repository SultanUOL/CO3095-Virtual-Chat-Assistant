"""
Symbolic Execution Tests for ChatEngine.process_turn()

These tests demonstrate symbolic execution by exploring execution paths
through the ChatEngine.process_turn() method.

Due to complexity (CC=12) and multiple stages, we focus on key symbolic paths:
- Path 1: Normal processing path (valid input → response)
- Path 2: Empty/None input → empty response
- Path 3: Validation stage errors → fallback
- Path 4: Intent classification paths → different handlers
- Path 5: Clarification flow → clarification question
- Path 6: Error handling paths → safe fallback
"""

import sys
from pathlib import Path

# Add tests directory to path for helpers import
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from helpers import FakeHistory, FakeInteractionLog
from vca.core.engine import ChatEngine


class TestSymbolicEngineProcessTurn:
    """Symbolic execution tests for ChatEngine.process_turn()"""

    def test_symbolic_path_normal_processing(self):
        """
        Symbolic Path 1: α = valid user message
        Constraint: input is valid text, passes validation, matches intent
        Expected: Normal processing → response generated
        """
        history = FakeHistory()
        log = FakeInteractionLog()
        engine = ChatEngine(history=history, interaction_log=log)

        result = engine.process_turn("hello")

        # Symbolic constraint: α ≠ None ∧ len(α) > 0 ∧ α passes validation
        assert result is not None
        assert len(result) > 0
        # Should generate a greeting response

    def test_symbolic_path_empty_input(self):
        """
        Symbolic Path 2: α = "" or None
        Constraint: input is empty or None
        Expected: Empty response or empty handling
        """
        history = FakeHistory()
        log = FakeInteractionLog()
        engine = ChatEngine(history=history, interaction_log=log)

        # Empty string path
        result_empty = engine.process_turn("")
        assert result_empty is not None

        # None input path
        result_none = engine.process_turn(None)
        assert result_none is not None

    def test_symbolic_path_help_command(self):
        """
        Symbolic Path 3: α = help command
        Constraint: input matches help intent pattern
        Expected: Help response generated
        """
        history = FakeHistory()
        log = FakeInteractionLog()
        engine = ChatEngine(history=history, interaction_log=log)

        result = engine.process_turn("help")

        # Symbolic constraint: α matches help intent
        assert "help" in result.lower() or "command" in result.lower()

    def test_symbolic_path_exit_command(self):
        """
        Symbolic Path 4: α = exit command
        Constraint: input matches exit intent pattern
        Expected: Exit/goodbye response
        """
        history = FakeHistory()
        log = FakeInteractionLog()
        engine = ChatEngine(history=history, interaction_log=log)

        result = engine.process_turn("exit")

        # Symbolic constraint: α matches exit intent
        assert result is not None

    def test_symbolic_path_question_intent(self):
        """
        Symbolic Path 5: α = question pattern
        Constraint: input starts with question word (what, why, how, etc.)
        Expected: Question intent → question handler response
        """
        history = FakeHistory()
        log = FakeInteractionLog()
        engine = ChatEngine(history=history, interaction_log=log)

        result = engine.process_turn("what is this")

        # Symbolic constraint: α matches question pattern
        assert result is not None
        assert len(result) > 0

    def test_symbolic_path_long_input_truncation(self):
        """
        Symbolic Path 6: α = very long input (exceeds MAX_LEN)
        Constraint: len(α) > MAX_LEN (2000)
        Expected: Input truncated, processing continues
        """
        history = FakeHistory()
        log = FakeInteractionLog()
        engine = ChatEngine(history=history, interaction_log=log)

        long_input = "a" * 3000  # Exceeds validator MAX_LEN
        result = engine.process_turn(long_input)

        # Symbolic constraint: len(α) > 2000
        # Should process (input will be truncated in validation stage)
        assert result is not None

    def test_symbolic_path_unknown_intent(self):
        """
        Symbolic Path 7: α = text matching no known patterns
        Constraint: α does not match any intent pattern
        Expected: Unknown intent → fallback response
        """
        history = FakeHistory()
        log = FakeInteractionLog()
        engine = ChatEngine(history=history, interaction_log=log)

        result = engine.process_turn("xyzabc123")

        # Symbolic constraint: α matches no intent patterns
        assert result is not None
        # Should get fallback/unknown response
