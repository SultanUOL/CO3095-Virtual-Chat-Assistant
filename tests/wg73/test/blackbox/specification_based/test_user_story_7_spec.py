# Test file for User Story 7
# Testing Type: blackbox
# Technique: specification_based
# Team Member: wg73
# Original file: test_user_story_7.py

from vca.core.responses import ResponseGenerator

def test_faq_how_is_history_stored() -> None:
    r = ResponseGenerator()
    assert (
        r.faq_response_for("how is history stored")
        == "History is stored in a JSONL file at data/history.jsonl (appended after each turn)."
    )
    assert (
        r.faq_response_for("HOW IS HISTORY STORED ")
        == "History is stored in a JSONL file at data/history.jsonl (appended after each turn)."
    )
