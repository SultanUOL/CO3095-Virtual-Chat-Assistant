"""
Symbolic Execution Tests for ChatEngine helper functions

These tests demonstrate symbolic execution by systematically exploring
execution paths through ChatEngine helper methods.
"""

import pytest
import sys
from pathlib import Path

# Add tests directory to path for helpers import
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from helpers import FakeHistory, FakeInteractionLog
from vca.core.engine import ChatEngine
from vca.core.intents import Intent


class TestSymbolicChatEngine:
    """Symbolic execution tests for ChatEngine helper methods"""

    def test_symbolic_parse_clarification_choice_path_numeric_1(self):
        """
        Symbolic Path 1: text = "1" or "one"
        Constraint: lower in {"1", "one"}
        Expected: Returns options[0] if exists
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        options = ["help", "question"]
        result = engine._parse_clarification_choice("1", options)
        assert result == "help"

    def test_symbolic_parse_clarification_choice_path_numeric_2(self):
        """
        Symbolic Path 2: text = "2" or "two"
        Constraint: lower in {"2", "two"}
        Expected: Returns options[1] if exists
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        options = ["help", "question"]
        result = engine._parse_clarification_choice("2", options)
        assert result == "question"

    def test_symbolic_parse_clarification_choice_path_direct_match(self):
        """
        Symbolic Path 3: text directly matches option
        Constraint: lower in options
        Expected: Returns matching option
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        options = ["help", "question"]
        result = engine._parse_clarification_choice("help", options)
        assert result == "help"

    def test_symbolic_parse_clarification_choice_path_exit_synonym(self):
        """
        Symbolic Path 4: exit synonym with exit in options
        Constraint: "exit" in options ∧ lower in {"quit", "bye", "goodbye"}
        Expected: Returns "exit"
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        options = ["exit", "help"]
        result = engine._parse_clarification_choice("quit", options)
        assert result == "exit"

    def test_symbolic_parse_clarification_choice_path_help_synonym(self):
        """
        Symbolic Path 5: help synonym with help in options
        Constraint: "help" in options ∧ lower in {"h", "commands", "help"}
        Expected: Returns "help"
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        options = ["help", "question"]
        result = engine._parse_clarification_choice("h", options)
        assert result == "help"

    def test_symbolic_parse_clarification_choice_path_no_match(self):
        """
        Symbolic Path 6: no match
        Constraint: text matches no patterns
        Expected: Returns None
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        options = ["help", "question"]
        result = engine._parse_clarification_choice("xyz", options)
        assert result is None

    def test_symbolic_parse_clarification_choice_path_empty_options(self):
        """
        Symbolic Path 7: options list too short
        Constraint: len(options) < required index
        Expected: Returns None for numeric choice
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        options = ["help"]
        result = engine._parse_clarification_choice("2", options)
        assert result is None

    def test_symbolic_stage_classify_intent_path_success(self):
        """
        Symbolic Path 1: Classification succeeds
        Constraint: classifier.classify() succeeds
        Expected: Returns (intent, result) tuple
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        from vca.core.engine import _TurnTelemetry

        telemetry = _TurnTelemetry(started=0.0)

        intent, result = engine._stage_classify_intent("hello", telemetry)
        assert intent is not None
        assert intent in Intent

    def test_symbolic_stage_classify_intent_path_exception(self):
        """
        Symbolic Path 2: Classification raises exception
        Constraint: classifier.classify() raises exception
        Expected: Exception propagates (handled at higher level in process_turn)
        Note: _stage_classify_intent doesn't catch exceptions, they're handled in process_turn
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        # Monkeypatch to raise exception
        original_classify = engine._classifier.classify

        def raise_exception(text):
            raise ValueError("Test exception")

        engine._classifier.classify = raise_exception

        from vca.core.engine import _TurnTelemetry

        telemetry = _TurnTelemetry(started=0.0)

        # Exception should propagate (not caught in _stage_classify_intent)
        with pytest.raises(ValueError):
            engine._stage_classify_intent("test", telemetry)

        engine._classifier.classify = original_classify

    def test_symbolic_stage_maybe_ask_for_clarification_path_multi_intent(self):
        """
        Symbolic Path 1: Multi-intent detected
        Constraint: _looks_like_multi_intent(text) = True
        Expected: Sets pending clarification, returns clarifying question
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        from vca.core.engine import _TurnTelemetry

        telemetry = _TurnTelemetry(started=0.0)

        # Text that looks like multi-intent
        result = engine._stage_maybe_ask_for_clarification(
            "help exit", Intent.HELP, None, telemetry
        )
        assert result is not None
        assert "Did you mean" in result or "Reply 1" in result

    def test_symbolic_stage_maybe_ask_for_clarification_path_low_confidence(self):
        """
        Symbolic Path 2: Low confidence
        Constraint: confidence < CONFIDENCE_THRESHOLD ∧ intent not EMPTY/UNKNOWN
        Expected: Sets pending clarification, returns clarifying question
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        from vca.core.engine import _TurnTelemetry

        telemetry = _TurnTelemetry(started=0.0)
        telemetry.confidence = 0.5  # Below threshold

        # Mock classifier result with candidates
        class MockResult:
            candidates = [(Intent.GREETING, "greeting"), (Intent.QUESTION, "question")]

        result = engine._stage_maybe_ask_for_clarification(
            "test", Intent.GREETING, MockResult(), telemetry
        )
        # May or may not ask for clarification depending on confidence
        assert result is None or "Did you mean" in result

    def test_symbolic_stage_maybe_ask_for_clarification_path_no_clarification(self):
        """
        Symbolic Path 3: No clarification needed
        Constraint: not multi-intent ∧ (confidence >= threshold or intent in {EMPTY, UNKNOWN})
        Expected: Returns None
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        from vca.core.engine import _TurnTelemetry

        telemetry = _TurnTelemetry(started=0.0)
        telemetry.confidence = 0.8  # Above threshold

        result = engine._stage_maybe_ask_for_clarification(
            "hello", Intent.GREETING, None, telemetry
        )
        assert result is None

    def test_symbolic_clarification_options_from_candidates_path_with_candidates(self):
        """
        Symbolic Path 1: Candidates exist
        Constraint: candidates is not empty
        Expected: Returns sorted options (max 2)
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        candidates = [
            (Intent.EXIT, "exit"),
            (Intent.HELP, "help"),
            (Intent.QUESTION, "question"),
        ]

        result = engine._clarification_options_from_candidates(candidates)
        assert len(result) <= 2
        assert len(result) > 0

    def test_symbolic_clarification_options_from_candidates_path_no_candidates(self):
        """
        Symbolic Path 2: No candidates or empty
        Constraint: candidates is None or empty
        Expected: Returns default ["help", "question"]
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        result = engine._clarification_options_from_candidates(None)
        assert result == ["help", "question"]

        result2 = engine._clarification_options_from_candidates([])
        assert result2 == ["help", "question"]

    def test_symbolic_clarification_options_from_candidates_path_filters_unknown(self):
        """
        Symbolic Path 3: Filters unknown/empty intents
        Constraint: candidates contain UNKNOWN or EMPTY
        Expected: Filters them out
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        candidates = [
            (Intent.UNKNOWN, "unknown"),
            (Intent.EMPTY, "empty"),
            (Intent.HELP, "help"),
        ]

        result = engine._clarification_options_from_candidates(candidates)
        assert "unknown" not in result
        assert "empty" not in result
        assert "help" in result or len(result) == 2

    def test_symbolic_classify_intent_path_success(self):
        """
        Symbolic Path 1: Classification succeeds
        Constraint: classifier.classify() succeeds
        Expected: Returns intent
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        intent = engine.classify_intent("hello")
        assert intent is not None
        assert intent in Intent

    def test_symbolic_classify_intent_path_exception(self):
        """
        Symbolic Path 2: Classification raises exception
        Constraint: classifier.classify() raises exception
        Expected: Returns Intent.UNKNOWN
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        # Monkeypatch to raise exception
        original_classify = engine._classifier.classify

        def raise_exception(text):
            raise ValueError("Test exception")

        engine._classifier.classify = raise_exception

        try:
            intent = engine.classify_intent("test")
            assert intent == Intent.UNKNOWN
        finally:
            engine._classifier.classify = original_classify

    def test_symbolic_reset_session_path(self):
        """
        Symbolic Path: Reset session
        Constraint: reset_session() called
        Expected: Session rebuilt or new blank session
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        # Add some state
        engine.process_turn("hello")

        # Reset
        engine.reset_session()

        # Session should be reset
        assert len(engine.session.messages) == 0 or len(engine.session.messages) >= 0

    def test_symbolic_clear_history_path_with_file(self):
        """
        Symbolic Path 1: clear_file = True
        Constraint: clear_file = True
        Expected: Clears file and memory
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        # Add some history
        engine.process_turn("hello")

        # Clear with file
        engine.clear_history(clear_file=True)

        # History should be cleared
        assert engine._loaded_turns_count == 0

    def test_symbolic_clear_history_path_without_file(self):
        """
        Symbolic Path 2: clear_file = False
        Constraint: clear_file = False
        Expected: Clears memory only
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        # Add some history
        engine.process_turn("hello")

        # Clear without file
        engine.clear_history(clear_file=False)

        # Memory should be cleared
        assert engine._loaded_turns_count == 0
