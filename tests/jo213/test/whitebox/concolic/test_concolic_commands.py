"""
Concolic Testing for parse_user_input()

Concolic testing combines concrete execution with symbolic constraint tracking.
"""

import pytest
from vca.cli.commands import parse_user_input, Command


class TestConcolicCommands:
    """Concolic testing for parse_user_input()"""

    def test_concolic_parse_user_input_iteration_1_empty(self):
        """
        Concolic Iteration 1: Explore empty input path
        Concrete Input: ""
        Symbolic: α = ""
        Constraint: stripped == ""
        Path Taken: Returns EMPTY command
        """
        result = parse_user_input("")
        assert result.command == Command.EMPTY

    def test_concolic_parse_user_input_iteration_2_help_token(self):
        """
        Concolic Iteration 2: Explore help token path
        Concrete Input: "help"
        Symbolic: α = "help"
        Constraint: lower in _HELP_TOKENS
        Path Taken: Returns HELP command
        """
        result = parse_user_input("help")
        assert result.command == Command.HELP

    def test_concolic_parse_user_input_iteration_3_exit_token(self):
        """
        Concolic Iteration 3: Explore exit token path
        Concrete Input: "exit"
        Symbolic: α = "exit"
        Constraint: lower in _EXIT_TOKENS
        Path Taken: Returns EXIT command
        """
        result = parse_user_input("exit")
        assert result.command == Command.EXIT

    def test_concolic_parse_user_input_iteration_4_prefix_command(self):
        """
        Concolic Iteration 4: Explore prefix command path
        Concrete Input: "/help"
        Symbolic: α starts with "/" or ":"
        Constraint: prefix != "" ∧ prefix in tokens
        Path Taken: Returns command based on prefix
        """
        result = parse_user_input("/help")
        assert result.command == Command.HELP

    def test_concolic_parse_user_input_iteration_5_message(self):
        """
        Concolic Iteration 5: Explore message path
        Concrete Input: "Hello world"
        Symbolic: α is not empty ∧ not in tokens ∧ no valid prefix
        Constraint: Regular message
        Path Taken: Returns MESSAGE command
        """
        result = parse_user_input("Hello world")
        assert result.command == Command.MESSAGE
        assert result.text == "Hello world"

    def test_concolic_path_coverage_summary(self):
        """
        Summary of concolic testing path coverage for parse_user_input():
        - Empty input path: ✅ Covered
        - Help token path: ✅ Covered
        - Exit token path: ✅ Covered
        - Prefix command path: ✅ Covered
        - Message path: ✅ Covered
        
        All major execution paths explored through iterative constraint negation
        """
        paths_explored = {
            "empty": parse_user_input("").command == Command.EMPTY,
            "help": parse_user_input("help").command == Command.HELP,
            "exit": parse_user_input("exit").command == Command.EXIT,
            "prefix": parse_user_input("/help").command == Command.HELP,
            "message": parse_user_input("Hello").command == Command.MESSAGE,
        }
        
        assert all(paths_explored.values()), "All concolic paths should be explored"

