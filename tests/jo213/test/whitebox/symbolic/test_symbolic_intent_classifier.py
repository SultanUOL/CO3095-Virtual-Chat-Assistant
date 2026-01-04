"""
Symbolic Execution Tests for IntentClassifier.classify_result()

These tests demonstrate symbolic execution by exploring key execution paths
through the IntentClassifier.classify_result() method.

Due to high complexity (CC=32), we focus on major symbolic paths:
- Path 1: empty input → EMPTY intent
- Path 2: exact command match → high confidence intent
- Path 3: phrase/token match → medium confidence intent
- Path 4: question prefix → QUESTION intent
- Path 5: no match → UNKNOWN intent
"""

from vca.core.intents import IntentClassifier, Intent


class TestSymbolicIntentClassifier:
    """Symbolic execution tests for IntentClassifier.classify_result()"""

    def test_symbolic_path_empty_input(self):
        """
        Symbolic Path 1: α = "" or None
        Constraint: stripped input is empty string
        Expected: IntentResult(Intent.EMPTY, confidence=1.0)
        """
        classifier = IntentClassifier()
        result = classifier.classify_result("")

        assert result.intent == Intent.EMPTY
        assert result.confidence == 1.0
        assert result.rule == "empty_input"

    def test_symbolic_path_none_input(self):
        """
        Symbolic Path: α = None
        Constraint: input is None
        Expected: IntentResult(Intent.EMPTY, confidence=1.0)
        """
        classifier = IntentClassifier()
        result = classifier.classify_result(None)

        assert result.intent == Intent.EMPTY
        assert result.confidence == 1.0

    def test_symbolic_path_exact_command_match(self):
        """
        Symbolic Path 2: α matches exact command token
        Constraint: input is exact command (e.g., "help", "exit")
        Expected: High confidence intent match
        """
        classifier = IntentClassifier()

        # Test exact "help" command
        result = classifier.classify_result("help")
        assert result.intent == Intent.HELP
        assert result.confidence >= 0.9  # Exact commands have high confidence

    def test_symbolic_path_phrase_match(self):
        """
        Symbolic Path 3: α matches phrase pattern
        Constraint: input matches phrase in synonym groups
        Expected: Intent match with phrase rule
        """
        classifier = IntentClassifier()

        # Test greeting phrase
        result = classifier.classify_result("hello")
        assert result.intent == Intent.GREETING
        assert result.rule == "greeting_phrase"

    def test_symbolic_path_question_prefix(self):
        """
        Symbolic Path 4: α starts with question prefix
        Constraint: input starts with question word (what, why, how, etc.)
        Expected: IntentResult(Intent.QUESTION, ...)
        """
        classifier = IntentClassifier()

        result = classifier.classify_result("what is this")
        assert result.intent == Intent.QUESTION
        assert "question" in result.rule.lower()

    def test_symbolic_path_no_match(self):
        """
        Symbolic Path 5: α matches no patterns
        Constraint: input matches no known patterns
        Expected: IntentResult(Intent.UNKNOWN, confidence ~0.2)
        """
        classifier = IntentClassifier()

        result = classifier.classify_result("xyzabc123")
        assert result.intent == Intent.UNKNOWN
        assert result.confidence <= 0.3  # Unknown has low confidence

    def test_symbolic_path_whitespace_only(self):
        """
        Symbolic Path: α contains only whitespace
        Constraint: input becomes empty after stripping
        Expected: IntentResult(Intent.EMPTY, ...)
        """
        classifier = IntentClassifier()

        result = classifier.classify_result("   ")
        assert result.intent == Intent.EMPTY

    def test_symbolic_path_case_insensitive_match(self):
        """
        Symbolic Path: α matches pattern but different case
        Constraint: input matches pattern when casefolded
        Expected: Intent match (case insensitive)
        """
        classifier = IntentClassifier()

        result = classifier.classify_result("HELLO")
        assert result.intent == Intent.GREETING

    def test_symbolic_path_multiple_matches_priority(self):
        """
        Symbolic Path: α matches multiple patterns
        Constraint: input matches patterns with different priorities
        Expected: Highest priority intent selected
        """
        classifier = IntentClassifier()

        # "exit" should have higher priority than "goodbye"
        result = classifier.classify_result("exit")
        assert result.intent == Intent.EXIT
        assert result.confidence >= 0.9

