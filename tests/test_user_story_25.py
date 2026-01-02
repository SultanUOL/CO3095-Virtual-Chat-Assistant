import json
from pathlib import Path

from vca.storage.history_store import HistoryStore


def test_us25_history_jsonl_records_include_ts_role_content(tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p)

    store.save_turn("hello", "Hi there")

    lines = store.load_history()
    assert len(lines) == 2  # user + assistant records

    first = json.loads(lines[0])
    second = json.loads(lines[1])

    for rec in (first, second):
        assert "ts" in rec
        assert "role" in rec
        assert "content" in rec

    assert first["role"] == "user"
    assert first["content"] == "hello"
    assert second["role"] == "assistant"
    assert second["content"] == "Hi there"


def test_us25_jsonl_round_trip_preserves_special_chars_and_newlines(
    tmp_path: Path,
) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p)

    user = 'line1\nline2 "quoted" ✅'
    assistant = "a\n\tb\r\nend"
    store.save_turn(user, assistant)

    turns = store.load_turns()
    assert len(turns) == 1
    assert turns[0].user_text == user
    assert turns[0].assistant_text == assistant


def test_us25_jsonl_loading_reconstructs_same_turns_order(tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p)

    store.save_turn("u1", "a1")
    store.save_turn("u2", "a2")
    store.save_turn("u3", "a3")

    turns = store.load_turns()
    assert [(t.user_text, t.assistant_text) for t in turns] == [
        ("u1", "a1"),
        ("u2", "a2"),
        ("u3", "a3"),
    ]
