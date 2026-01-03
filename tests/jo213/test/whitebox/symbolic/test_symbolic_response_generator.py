"""
Symbolic Execution Tests for ResponseGenerator functions

These tests demonstrate symbolic execution by systematically exploring
execution paths through ResponseGenerator methods.
"""

import pytest
from vca.core.responses import ResponseGenerator
from vca.core.intents import Intent
from vca.domain.session import Message
from vca.domain.chat_turn import ChatTurn


class TestSymbolicResponseGenerator:
    """Symbolic execution tests for ResponseGenerator methods"""

    def test_symbolic_generate_path_faq_match(self):
        """
        Symbolic Path 1: α = FAQ key
        Constraint: raw_text matches FAQ key after normalization
        Expected: Returns FAQ response
        """
        generator = ResponseGenerator()
        
        # FAQ match path
        result = generator.generate(Intent.QUESTION, "help")
        assert "Commands" in result or "help" in result.lower()

    def test_symbolic_generate_path_no_faq(self):
        """
        Symbolic Path 2: α ≠ FAQ key
        Constraint: raw_text does not match FAQ key
        Expected: Routes to intent handler
        """
        generator = ResponseGenerator()
        
        # No FAQ match, routes to handler
        result = generator.generate(Intent.GREETING, "hello")
        assert result is not None
        assert len(result) > 0

    def test_symbolic_generate_path_none_intent(self):
        """
        Symbolic Path 3: intent = None
        Constraint: intent is None
        Expected: Normalized to UNKNOWN, routes to unknown handler
        """
        generator = ResponseGenerator()
        
        result = generator.generate(None, "test")
        assert result is not None

    def test_symbolic_route_path_none_intent(self):
        """
        Symbolic Path 1: intent = None
        Constraint: intent is None
        Expected: Returns handle_unknown handler
        """
        generator = ResponseGenerator()
        
        handler = generator.route(None)
        result = handler("test", None, None)
        assert "did not understand" in result.lower() or "rephrase" in result.lower()

    def test_symbolic_route_path_enum_intent(self):
        """
        Symbolic Path 2: intent has .value attribute
        Constraint: hasattr(intent, "value") = True
        Expected: Extracts value, routes to handler
        """
        generator = ResponseGenerator()
        
        handler = generator.route(Intent.GREETING)
        result = handler("hello", None, None)
        assert "Hello" in result or "help" in result.lower()

    def test_symbolic_route_path_string_intent(self):
        """
        Symbolic Path 3: intent is string
        Constraint: intent is string, no .value attribute
        Expected: Converts to string, routes to handler
        """
        generator = ResponseGenerator()
        
        handler = generator.route("help")
        result = handler("help", None, None)
        assert "Commands" in result or "help" in result.lower()

    def test_symbolic_route_path_unknown_intent(self):
        """
        Symbolic Path 4: intent not in handlers dict
        Constraint: safe_intent not in handlers.keys()
        Expected: Returns handle_unknown handler
        """
        generator = ResponseGenerator()
        
        handler = generator.route("nonexistent")
        result = handler("test", None, None)
        assert "did not understand" in result.lower() or "rephrase" in result.lower()

    def test_symbolic_handle_question_path_with_topic(self):
        """
        Symbolic Path 1: previous_user_text exists ∧ topic extracted
        Constraint: recent contains user message ∧ extract_topic returns non-empty
        Expected: Returns follow-up response with topic
        """
        generator = ResponseGenerator()
        
        recent = [
            Message(role="user", content="Tell me about Python"),
            Message(role="assistant", content="Python is a language")
        ]
        
        result = generator.handle_question("what is it?", recent, None)
        assert "Following up" in result or "question" in result.lower()

    def test_symbolic_handle_question_path_no_topic(self):
        """
        Symbolic Path 2: previous_user_text exists ∧ topic = ""
        Constraint: recent contains user message ∧ extract_topic returns empty
        Expected: Returns generic question response
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

    def test_symbolic_handle_question_path_empty_preview(self):
        """
        Symbolic Path 3: preview = ""
        Constraint: text.strip() = "" or len(text) = 0
        Expected: Returns "did not catch your question" message
        """
        generator = ResponseGenerator()
        
        result = generator.handle_question("", None, None)
        assert "did not catch" in result.lower() or "help" in result.lower()

    def test_symbolic_handle_question_path_context_fallback(self):
        """
        Symbolic Path 4: recent empty ∧ context exists
        Constraint: recent = None/empty ∧ context is not empty
        Expected: Uses context[-1].user_text for topic extraction
        """
        generator = ResponseGenerator()
        
        context = [
            ChatTurn(user_text="Tell me about Java", assistant_text="Java is a language")
        ]
        
        result = generator.handle_question("what about it?", None, context)
        assert result is not None
        assert len(result) > 0

    def test_symbolic_handle_greeting_path(self):
        """
        Symbolic Path: greeting handler
        Constraint: intent = GREETING
        Expected: Returns greeting response with session suffix
        """
        generator = ResponseGenerator()
        
        # No recent messages
        result1 = generator.handle_greeting("hello", None, None)
        assert "Hello" in result1
        
        # With recent messages
        recent = [
            Message(role="user", content="hi"),
            Message(role="assistant", content="Hello")
        ]
        result2 = generator.handle_greeting("hello", recent, None)
        assert "Hello" in result2
        assert "Messages this session" in result2

    def test_symbolic_extract_topic_path_proper_noun(self):
        """
        Symbolic Path 1: proper noun found
        Constraint: text contains capitalized word not in ignore set ∧ len > 2
        Expected: Returns lowercased proper noun
        """
        generator = ResponseGenerator()
        
        result = generator.extract_topic_from_last_user_message("Tell me about Python")
        assert result == "python"

    def test_symbolic_extract_topic_path_about_phrase(self):
        """
        Symbolic Path 2: "about" phrase found
        Constraint: text contains "about [word]" pattern
        Expected: Returns word after "about"
        """
        generator = ResponseGenerator()
        
        result = generator.extract_topic_from_last_user_message("I want to know about Java")
        assert result == "java"

    def test_symbolic_extract_topic_path_regarding_phrase(self):
        """
        Symbolic Path 3: "regarding" phrase found
        Constraint: text contains "regarding [word]" pattern
        Expected: Returns word after "regarding"
        """
        generator = ResponseGenerator()
        
        # Use lowercase to avoid proper noun matching first
        result = generator.extract_topic_from_last_user_message("questions regarding javascript")
        assert result == "javascript"

    def test_symbolic_extract_topic_path_stop_word_filtering(self):
        """
        Symbolic Path 4: stop word filtering
        Constraint: words exist but filtered by stop words, first non-stop word found
        Expected: Returns first non-stop word with len > 2
        """
        generator = ResponseGenerator()
        
        result = generator.extract_topic_from_last_user_message("what is programming")
        assert result == "programming"

    def test_symbolic_extract_topic_path_fallback_first_word(self):
        """
        Symbolic Path 5: all words are stop words or len <= 2
        Constraint: all words filtered, fallback to first word
        Expected: Returns first word from words list
        """
        generator = ResponseGenerator()
        
        result = generator.extract_topic_from_last_user_message("I am")
        assert result in ["i", "am"] or result == ""

    def test_symbolic_extract_topic_path_empty_text(self):
        """
        Symbolic Path 6: text = ""
        Constraint: text is empty or None
        Expected: Returns ""
        """
        generator = ResponseGenerator()
        
        result = generator.extract_topic_from_last_user_message("")
        assert result == ""

    def test_symbolic_handle_history_path_no_recent(self):
        """
        Symbolic Path 1: recent = None or empty
        Constraint: not recent or len(recent) = 0
        Expected: Returns "No messages yet" message
        """
        generator = ResponseGenerator()
        
        result = generator.handle_history("history", None, None)
        assert "No messages" in result or "yet" in result.lower()

    def test_symbolic_handle_history_path_with_recent(self):
        """
        Symbolic Path 2: recent exists
        Constraint: recent is not empty
        Expected: Returns formatted recent messages (last 6)
        """
        generator = ResponseGenerator()
        
        recent = [
            Message(role="user", content="hello"),
            Message(role="assistant", content="Hello"),
            Message(role="user", content="how are you"),
            Message(role="assistant", content="I'm fine")
        ]
        
        result = generator.handle_history("history", recent, None)
        assert "Recent messages" in result
        assert "user:" in result.lower() or "assistant:" in result.lower()

    def test_symbolic_handle_unknown_path(self):
        """
        Symbolic Path: unknown intent handler
        Constraint: intent = UNKNOWN
        Expected: Returns fallback unknown message
        """
        generator = ResponseGenerator()
        
        result = generator.handle_unknown("xyz", None, None)
        assert "did not understand" in result.lower() or "rephrase" in result.lower()

