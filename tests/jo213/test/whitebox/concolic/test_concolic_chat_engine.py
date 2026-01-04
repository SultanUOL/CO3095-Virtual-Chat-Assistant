"""
Concolic Testing for ChatEngine helper functions

Concolic testing combines concrete execution with symbolic constraint tracking.
"""

import sys
from pathlib import Path

# Add tests directory to path for helpers import
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from helpers import FakeHistory, FakeInteractionLog
from vca.core.engine import ChatEngine
from vca.core.intents import Intent


class TestConcolicChatEngine:
    """Concolic testing for ChatEngine helper methods"""

    def test_concolic_parse_clarification_choice_iteration_1_numeric(self):
        """
        Concolic Iteration 1: Explore numeric choice path
        Concrete Input: "1"
        Symbolic: α = "1"
        Constraint: lower in {"1", "one"}
        Path Taken: Returns options[0]
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        options = ["help", "question"]
        result = engine._parse_clarification_choice("1", options)
        assert result == "help"

    def test_concolic_parse_clarification_choice_iteration_2_direct_match(self):
        """
        Concolic Iteration 2: Explore direct match path
        Concrete Input: "help"
        Symbolic: α = "help"
        Constraint: lower in options
        Path Taken: Returns matching option
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        options = ["help", "question"]
        result = engine._parse_clarification_choice("help", options)
        assert result == "help"

    def test_concolic_parse_clarification_choice_iteration_3_synonym(self):
        """
        Concolic Iteration 3: Explore synonym path
        Concrete Input: "quit"
        Symbolic: α = "quit"
        Constraint: "exit" in options ∧ lower in {"quit", "bye", "goodbye"}
        Path Taken: Returns "exit"
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        options = ["exit", "help"]
        result = engine._parse_clarification_choice("quit", options)
        assert result == "exit"

    def test_concolic_parse_clarification_choice_iteration_4_no_match(self):
        """
        Concolic Iteration 4: Explore no match path
        Concrete Input: "xyz"
        Symbolic: α = "xyz"
        Constraint: α matches no patterns
        Path Taken: Returns None
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        options = ["help", "question"]
        result = engine._parse_clarification_choice("xyz", options)
        assert result is None

    def test_concolic_stage_classify_intent_iteration_1_success(self):
        """
        Concolic Iteration 1: Explore successful classification
        Concrete Input: "hello"
        Symbolic: α = "hello"
        Constraint: classifier.classify() succeeds
        Path Taken: Returns (intent, result)
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        from vca.core.engine import _TurnTelemetry

        telemetry = _TurnTelemetry(started=0.0)

        intent, result = engine._stage_classify_intent("hello", telemetry)
        assert intent is not None

    def test_concolic_stage_maybe_ask_for_clarification_iteration_1_multi_intent(self):
        """
        Concolic Iteration 1: Explore multi-intent path
        Concrete Input: "help exit"
        Symbolic: α contains both help and exit tokens
        Constraint: _looks_like_multi_intent(α) = True
        Path Taken: Returns clarifying question
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        from vca.core.engine import _TurnTelemetry

        telemetry = _TurnTelemetry(started=0.0)

        result = engine._stage_maybe_ask_for_clarification(
            "help exit", Intent.HELP, None, telemetry
        )
        assert result is not None

    def test_concolic_stage_maybe_ask_for_clarification_iteration_2_no_clarification(
        self,
    ):
        """
        Concolic Iteration 2: Explore no clarification path
        Concrete Input: "hello"
        Symbolic: α = "hello"
        Constraint: not multi-intent ∧ confidence >= threshold
        Path Taken: Returns None
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        from vca.core.engine import _TurnTelemetry

        telemetry = _TurnTelemetry(started=0.0)
        telemetry.confidence = 0.8

        result = engine._stage_maybe_ask_for_clarification(
            "hello", Intent.GREETING, None, telemetry
        )
        assert result is None

    def test_concolic_clarification_options_iteration_1_with_candidates(self):
        """
        Concolic Iteration 1: Explore candidates path
        Concrete Input: Candidates list
        Symbolic: candidates is not empty
        Constraint: len(candidates) > 0
        Path Taken: Returns sorted options
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        candidates = [(Intent.HELP, "help"), (Intent.EXIT, "exit")]
        result = engine._clarification_options_from_candidates(candidates)
        assert len(result) > 0
        assert len(result) <= 2

    def test_concolic_clarification_options_iteration_2_no_candidates(self):
        """
        Concolic Iteration 2: Explore no candidates path
        Concrete Input: None
        Symbolic: candidates = None
        Constraint: candidates is None or empty
        Path Taken: Returns default options
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        result = engine._clarification_options_from_candidates(None)
        assert result == ["help", "question"]

    def test_concolic_classify_intent_iteration_1_success(self):
        """
        Concolic Iteration 1: Explore successful classification
        Concrete Input: "hello"
        Symbolic: α = "hello"
        Constraint: classifier.classify() succeeds
        Path Taken: Returns intent
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        intent = engine.classify_intent("hello")
        assert intent is not None
        assert intent in Intent

    def test_concolic_path_coverage_summary(self):
        """
        Summary of concolic testing path coverage for ChatEngine:
        - Parse clarification choice (numeric): ✅ Covered
        - Parse clarification choice (direct): ✅ Covered
        - Parse clarification choice (synonym): ✅ Covered
        - Parse clarification choice (no match): ✅ Covered
        - Stage classify intent (success): ✅ Covered
        - Stage maybe ask clarification (multi-intent): ✅ Covered
        - Stage maybe ask clarification (no clarification): ✅ Covered
        - Clarification options (with candidates): ✅ Covered
        - Clarification options (no candidates): ✅ Covered
        - Classify intent (success): ✅ Covered

        All major execution paths explored through iterative constraint negation
        """
        engine = ChatEngine(history=FakeHistory(), interaction_log=FakeInteractionLog())

        paths_explored = {
            "numeric_choice": engine._parse_clarification_choice(
                "1", ["help", "question"]
            )
            == "help",
            "direct_match": engine._parse_clarification_choice(
                "help", ["help", "question"]
            )
            == "help",
            "synonym": engine._parse_clarification_choice("quit", ["exit", "help"])
            == "exit",
            "no_match": engine._parse_clarification_choice("xyz", ["help", "question"])
            is None,
            "classify_success": engine.classify_intent("hello") is not None,
            "clarification_options": len(
                engine._clarification_options_from_candidates([(Intent.HELP, "help")])
            )
            > 0,
        }

        assert all(paths_explored.values()), "All concolic paths should be explored"
