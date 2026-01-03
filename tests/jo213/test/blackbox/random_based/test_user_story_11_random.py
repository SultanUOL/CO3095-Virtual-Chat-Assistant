# Test file for User Story 11
# Testing Type: blackbox
# Technique: random_based
# Team Member: jo213
# Original file: test_user_story_11.py

from pathlib import Path
from vca.domain.constants import HISTORY_MAX_TURNS
from vca.domain.session import ConversationSession
from vca.storage.history_store import HistoryStore

def test_session_trims_oldest_turns_in_memory() -> None:
    s = ConversationSession()

    for i in range(HISTORY_MAX_TURNS + 10):
        s.add_message("user", f"u{i}")
        s.add_message("assistant", f"a{i}")

    msgs = s.recent_messages(limit=10_000)
    assert len(msgs) == HISTORY_MAX_TURNS * 2
    assert msgs[0].content == "u10"
    assert msgs[1].content == "a10"

def test_history_file_is_trimmed_to_last_n_turns(tmp_path: Path) -> None:
    p = tmp_path / "history.txt"
    store = HistoryStore(path=p)

    for i in range(HISTORY_MAX_TURNS + 10):
        store.save_turn(f"u{i}", f"a{i}")

    text = p.read_text(encoding="utf-8")
    assert text.count("---\n") == HISTORY_MAX_TURNS
    assert f"u{HISTORY_MAX_TURNS + 9}" in text
    assert "u0" not in text
