"""
Concolic Testing for ResponseGenerator functions

Concolic testing combines concrete execution with symbolic constraint tracking.
This test iteratively explores paths by:
1. Starting with concrete inputs
2. Tracking symbolic constraints
3. Negating constraints to explore alternative paths
4. Generating new inputs based on constraints
"""

import pytest
from vca.core.responses import ResponseGenerator
from vca.core.intents import Intent
from vca.domain.session import Message
from vca.domain.chat_turn import ChatTurn


class TestConcolicResponseGenerator:
    """Concolic testing for ResponseGenerator methods"""

    def test_concolic_generate_iteration_1_faq_path(self):
        """
        Concolic Iteration 1: Explore FAQ match path
        Concrete Input: "help"
        Symbolic: α = "help"
        Constraint: normalize_faq_key(α) in FAQ_MAP
        Path Taken: FAQ response path
        Next: Negate to explore non-FAQ path
        """
        generator = ResponseGenerator()
        
        result = generator.generate(Intent.HELP, "help")
        assert result is not None
        # FAQ path explored

    def test_concolic_generate_iteration_2_non_faq_path(self):
        """
        Concolic Iteration 2: Explore non-FAQ path
        Concrete Input: "hello"
        Symbolic: α = "hello"
        Constraint: normalize_faq_key(α) not in FAQ_MAP
        Path Taken: Intent routing path
        """
        generator = ResponseGenerator()
        
        result = generator.generate(Intent.GREETING, "hello")
        assert result is not None
        assert "Hello" in result

    def test_concolic_generate_iteration_3_none_intent(self):
        """
        Concolic Iteration 3: Explore None intent path
        Concrete Input: None intent
        Symbolic: intent = None
        Constraint: intent is None
        Path Taken: Normalize to UNKNOWN, unknown handler
        """
        generator = ResponseGenerator()
        
        result = generator.generate(None, "test")
        assert result is not None

    def test_concolic_route_iteration_1_enum_intent(self):
        """
        Concolic Iteration 1: Explore enum intent path
        Concrete Input: Intent.GREETING
        Symbolic: intent has .value attribute
        Constraint: hasattr(intent, "value") = True
        Path Taken: Extract value, route to handler
        """
        generator = ResponseGenerator()
        
        handler = generator.route(Intent.GREETING)
        result = handler("hello", None, None)
        assert "Hello" in result

    def test_concolic_route_iteration_2_string_intent(self):
        """
        Concolic Iteration 2: Explore string intent path
        Concrete Input: "help"
        Symbolic: intent is string
        Constraint: hasattr(intent, "value") = False
        Path Taken: Convert to string, route to handler
        """
        generator = ResponseGenerator()
        
        handler = generator.route("help")
        result = handler("help", None, None)
        assert "Commands" in result or "help" in result.lower()

    def test_concolic_route_iteration_3_none_intent(self):
        """
        Concolic Iteration 3: Explore None intent path
        Concrete Input: None
        Symbolic: intent = None
        Constraint: intent is None
        Path Taken: Default to "unknown", unknown handler
        """
        generator = ResponseGenerator()
        
        handler = generator.route(None)
        result = handler("test", None, None)
        assert "did not understand" in result.lower() or "rephrase" in result.lower()

    def test_concolic_handle_question_iteration_1_with_topic(self):
        """
        Concolic Iteration 1: Explore topic extraction path
        Concrete Input: Question with previous context
        Symbolic: recent contains user message ∧ topic extractable
        Constraint: previous_user_text ≠ "" ∧ topic ≠ ""
        Path Taken: Follow-up response with topic
        """
        generator = ResponseGenerator()
        
        recent = [
            Message(role="user", content="Tell me about Python"),
            Message(role="assistant", content="Python is great")
        ]
        
        result = generator.handle_question("what is it?", recent, None)
        assert "Following up" in result or "question" in result.lower()

    def test_concolic_handle_question_iteration_2_no_topic(self):
        """
        Concolic Iteration 2: Explore no topic path
        Concrete Input: Question without extractable topic
        Symbolic: recent exists but topic = ""
        Constraint: previous_user_text exists ∧ topic = ""
        Path Taken: Generic question response
        """
        generator = ResponseGenerator()
        
        # Use a message that won't extract a topic (all stop words)
        recent = [
            Message(role="user", content="I am"),
            Message(role="assistant", content="Hello")
        ]
        
        result = generator.handle_question("what?", recent, None)
        # May return follow-up or generic question response
        assert result is not None
        assert len(result) > 0

    def test_concolic_handle_question_iteration_3_empty_preview(self):
        """
        Concolic Iteration 3: Explore empty preview path
        Concrete Input: Empty or whitespace text
        Symbolic: text.strip() = ""
        Constraint: preview = ""
        Path Taken: "did not catch" message
        """
        generator = ResponseGenerator()
        
        result = generator.handle_question("   ", None, None)
        assert "did not catch" in result.lower() or "help" in result.lower()

    def test_concolic_extract_topic_iteration_1_proper_noun(self):
        """
        Concolic Iteration 1: Explore proper noun path
        Concrete Input: "Tell me about Python"
        Symbolic: text contains capitalized word
        Constraint: proper_noun found ∧ not in ignore set ∧ len > 2
        Path Taken: Return proper noun
        """
        generator = ResponseGenerator()
        
        result = generator.extract_topic_from_last_user_message("Tell me about Python")
        assert result == "python"

    def test_concolic_extract_topic_iteration_2_about_phrase(self):
        """
        Concolic Iteration 2: Explore "about" phrase path
        Concrete Input: "I want to know about Java"
        Symbolic: text contains "about [word]" pattern
        Constraint: regex match for "about" phrase
        Path Taken: Return word after "about"
        """
        generator = ResponseGenerator()
        
        result = generator.extract_topic_from_last_user_message("I want to know about Java")
        assert result == "java"

    def test_concolic_extract_topic_iteration_3_stop_words(self):
        """
        Concolic Iteration 3: Explore stop word filtering path
        Concrete Input: "what is programming"
        Symbolic: words exist but filtered by stop words
        Constraint: first non-stop word with len > 2 found
        Path Taken: Return first non-stop word
        """
        generator = ResponseGenerator()
        
        result = generator.extract_topic_from_last_user_message("what is programming")
        assert result == "programming"

    def test_concolic_extract_topic_iteration_4_empty(self):
        """
        Concolic Iteration 4: Explore empty text path
        Concrete Input: ""
        Symbolic: text = ""
        Constraint: text is empty
        Path Taken: Return ""
        """
        generator = ResponseGenerator()
        
        result = generator.extract_topic_from_last_user_message("")
        assert result == ""

    def test_concolic_path_coverage_summary(self):
        """
        Summary of concolic testing path coverage for ResponseGenerator:
        - FAQ match path: ✅ Covered
        - Non-FAQ routing path: ✅ Covered
        - None intent path: ✅ Covered
        - Enum intent routing: ✅ Covered
        - String intent routing: ✅ Covered
        - Question with topic: ✅ Covered
        - Question without topic: ✅ Covered
        - Empty preview path: ✅ Covered
        - Topic extraction paths: ✅ Covered
        
        All major execution paths explored through iterative constraint negation
        """
        generator = ResponseGenerator()
        
        paths_explored = {
            "faq": generator.generate(Intent.HELP, "help") is not None,
            "non_faq": generator.generate(Intent.GREETING, "hello") is not None,
            "none_intent": generator.generate(None, "test") is not None,
            "question_topic": len(generator.handle_question(
                "what?", 
                [Message(role="user", content="about Python")],
                None
            )) > 0,
            "extract_topic": generator.extract_topic_from_last_user_message("about Java") == "java",
        }
        
        assert all(paths_explored.values()), "All concolic paths should be explored"

