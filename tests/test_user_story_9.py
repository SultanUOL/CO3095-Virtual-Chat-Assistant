from pathlib import Path

from vca.core.engine import ChatEngine
from vca.storage.history_store import HistoryStore


def test_history_store_creates_file_and_appends_lines(tmp_path: Path) -> None:
    history_path = tmp_path / "history.txt"
    store = HistoryStore(path=history_path)

    store.save_turn("hello", "Hi there")
    store.save_turn("how are you?", "I am fine")

    assert history_path.exists() is True

    lines = store.load_history()
    # Two turns => 3 lines per turn (USER, ASSISTANT, separator)
    assert len(lines) == 6
    assert "USER: hello" in lines[0]
    assert "ASSISTANT: Hi there" in lines[1]
    assert lines[2] == "---"
    assert "USER: how are you?" in lines[3]
    assert "ASSISTANT: I am fine" in lines[4]
    assert lines[5] == "---"


def test_load_history_returns_empty_when_missing(tmp_path: Path) -> None:
    store = HistoryStore(path=tmp_path / "does_not_exist.txt")
    assert store.load_history() == []


def test_engine_persists_history_non_fatal(tmp_path: Path) -> None:
    e = ChatEngine()
    e._history = HistoryStore(path=tmp_path / "history.txt")

    r = e.process_turn("hello")
    assert isinstance(r, str)

    lines = e._history.load_history()
    assert any("USER: hello" in line for line in lines)
    assert any("ASSISTANT:" in line for line in lines)
