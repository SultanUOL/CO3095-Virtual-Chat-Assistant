# Test file for User Story 6
# Testing Type: whitebox
# Technique: branch_coverage
# Team Member: wg73
# Original file: test_user_story_6.py

from vca.core.engine import ChatEngine

def test_routing_is_testable_without_cli() -> None:
    e = ChatEngine()

    help_handler = e.route_intent("help")
    out = help_handler("help", [])
    assert "Commands:" in out

    unknown_handler = e.route_intent("unknown")
    out2 = unknown_handler("hello", [])
    assert "type help" in out2
