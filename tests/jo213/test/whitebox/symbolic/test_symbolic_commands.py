"""
Symbolic Execution Tests for parse_user_input()

These tests demonstrate symbolic execution by systematically exploring
execution paths through parse_user_input() function.
"""

import pytest
from vca.cli.commands import parse_user_input, Command, ParsedInput


class TestSymbolicCommands:
    """Symbolic execution tests for parse_user_input()"""

    def test_symbolic_parse_user_input_path_empty(self):
        """
        Symbolic Path 1: Empty input
        Constraint: stripped == ""
        Expected: Returns ParsedInput(command=EMPTY, text="")
        """
        result = parse_user_input("")
        assert result.command == Command.EMPTY
        assert result.text == ""

    def test_symbolic_parse_user_input_path_none(self):
        """
        Symbolic Path 2: None input
        Constraint: raw_text is None
        Expected: Returns ParsedInput(command=EMPTY, text="")
        """
        result = parse_user_input(None)
        assert result.command == Command.EMPTY
        assert result.text == ""

    def test_symbolic_parse_user_input_path_help_token(self):
        """
        Symbolic Path 3: Help token
        Constraint: lower in _HELP_TOKENS
        Expected: Returns ParsedInput(command=HELP, text="help")
        """
        result = parse_user_input("help")
        assert result.command == Command.HELP
        assert result.text == "help"

    def test_symbolic_parse_user_input_path_exit_token(self):
        """
        Symbolic Path 4: Exit token
        Constraint: lower in _EXIT_TOKENS
        Expected: Returns ParsedInput(command=EXIT, text="exit")
        """
        result = parse_user_input("exit")
        assert result.command == Command.EXIT
        assert result.text == "exit"

    def test_symbolic_parse_user_input_path_restart_token(self):
        """
        Symbolic Path 5: Restart token
        Constraint: lower in _RESTART_TOKENS
        Expected: Returns ParsedInput(command=RESTART, text="restart")
        """
        result = parse_user_input("restart")
        assert result.command == Command.RESTART
        assert result.text == "restart"

    def test_symbolic_parse_user_input_path_prefix_help(self):
        """
        Symbolic Path 6: Prefix with help command
        Constraint: prefix != "" ∧ lower_prefix in _HELP_TOKENS
        Expected: Returns ParsedInput(command=HELP, text="help")
        """
        result = parse_user_input("/help")
        assert result.command == Command.HELP
        assert result.text == "help"

    def test_symbolic_parse_user_input_path_prefix_exit(self):
        """
        Symbolic Path 7: Prefix with exit command
        Constraint: prefix != "" ∧ lower_prefix in _EXIT_TOKENS
        Expected: Returns ParsedInput(command=EXIT, text="exit")
        """
        result = parse_user_input(":exit")
        assert result.command == Command.EXIT
        assert result.text == "exit"

    def test_symbolic_parse_user_input_path_prefix_unknown(self):
        """
        Symbolic Path 8: Prefix with unknown command
        Constraint: prefix != "" ∧ prefix not in known tokens
        Expected: Returns ParsedInput(command=UNKNOWN, text=prefix)
        """
        result = parse_user_input("/unknown")
        assert result.command == Command.UNKNOWN
        assert result.text == "unknown"

    def test_symbolic_parse_user_input_path_message(self):
        """
        Symbolic Path 9: Regular message
        Constraint: not empty ∧ not in tokens ∧ no prefix or prefix not in tokens
        Expected: Returns ParsedInput(command=MESSAGE, text=original)
        """
        result = parse_user_input("Hello, how are you?")
        assert result.command == Command.MESSAGE
        assert result.text == "Hello, how are you?"

    def test_symbolic_parse_user_input_path_case_insensitive(self):
        """
        Symbolic Path 10: Case insensitive matching
        Constraint: lower matches token regardless of case
        Expected: Matches token correctly
        """
        result1 = parse_user_input("HELP")
        assert result1.command == Command.HELP
        
        result2 = parse_user_input("Exit")
        assert result2.command == Command.EXIT


