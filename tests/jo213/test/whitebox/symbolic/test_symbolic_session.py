"""
Symbolic Execution Tests for ConversationSession functions

These tests demonstrate symbolic execution by systematically exploring
execution paths through ConversationSession methods.
"""

import pytest
from vca.domain.session import ConversationSession, Message
from vca.domain.chat_turn import ChatTurn


class TestSymbolicSession:
    """Symbolic execution tests for ConversationSession methods"""

    def test_symbolic_recent_turns_path_canonical_turns(self):
        """
        Symbolic Path 1: Canonical turns exist
        Constraint: len(self.turns) > 0
        Expected: Returns turns from canonical turns buffer
        """
        session = ConversationSession()
        
        turn1 = ChatTurn(user_text="hello", assistant_text="Hello")
        turn2 = ChatTurn(user_text="how are you", assistant_text="I'm fine")
        
        session.add_turn(turn1)
        session.add_turn(turn2)
        
        result = session.recent_turns(limit=2)
        assert len(result) == 2
        assert result[0] == turn1 or result[0] == turn2

    def test_symbolic_recent_turns_path_derive_from_messages(self):
        """
        Symbolic Path 2: No canonical turns, derive from messages
        Constraint: len(self.turns) = 0
        Expected: Derives turns from messages
        """
        session = ConversationSession()
        
        session.add_message("user", "hello")
        session.add_message("assistant", "Hello")
        session.add_message("user", "how are you")
        session.add_message("assistant", "I'm fine")
        
        result = session.recent_turns(limit=2)
        assert len(result) >= 1

    def test_symbolic_recent_turns_path_limit_application(self):
        """
        Symbolic Path 3: Limit applied
        Constraint: len(turns) > limit
        Expected: Returns only last N turns
        """
        session = ConversationSession()
        
        for i in range(5):
            session.add_turn(ChatTurn(user_text=f"msg{i}", assistant_text=f"resp{i}"))
        
        result = session.recent_turns(limit=2)
        assert len(result) == 2

    def test_symbolic_recent_turns_path_zero_limit(self):
        """
        Symbolic Path 4: limit = 0
        Constraint: limit <= 0
        Expected: Returns empty list
        """
        session = ConversationSession()
        
        session.add_turn(ChatTurn(user_text="hello", assistant_text="Hello"))
        
        result = session.recent_turns(limit=0)
        assert result == []

    def test_symbolic_set_pending_clarification_path_normal(self):
        """
        Symbolic Path 1: Normal clarification setup
        Constraint: original_text and options provided
        Expected: Sets pending_clarification state
        """
        session = ConversationSession()
        
        session.set_pending_clarification("help exit", ["help", "exit"])
        
        assert session.pending_clarification is not None
        assert session.pending_clarification.original_text == "help exit"
        assert "help" in session.pending_clarification.options
        assert "exit" in session.pending_clarification.options

    def test_symbolic_set_pending_clarification_path_empty_options_filtered(self):
        """
        Symbolic Path 2: Empty options filtered
        Constraint: options contain empty strings
        Expected: Filters out empty options
        """
        session = ConversationSession()
        
        session.set_pending_clarification("test", ["help", "", "  ", "exit"])
        
        assert session.pending_clarification is not None
        assert "" not in session.pending_clarification.options
        assert "  " not in session.pending_clarification.options

    def test_symbolic_set_pending_clarification_path_deduplication(self):
        """
        Symbolic Path 3: Duplicate options deduplicated
        Constraint: options contain duplicates
        Expected: Removes duplicates
        """
        session = ConversationSession()
        
        session.set_pending_clarification("test", ["help", "help", "exit", "exit"])
        
        assert session.pending_clarification is not None
        options = session.pending_clarification.options
        assert options.count("help") == 1
        assert options.count("exit") == 1

    def test_symbolic_set_pending_clarification_path_case_normalization(self):
        """
        Symbolic Path 4: Case normalization
        Constraint: options have mixed case
        Expected: Normalizes to lowercase
        """
        session = ConversationSession()
        
        session.set_pending_clarification("test", ["HELP", "Exit", "question"])
        
        assert session.pending_clarification is not None
        options = session.pending_clarification.options
        assert "help" in options
        assert "exit" in options
        assert "question" in options


