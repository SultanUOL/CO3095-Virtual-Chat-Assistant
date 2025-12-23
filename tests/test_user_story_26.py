import json
from pathlib import Path

from vca.storage.history_store import HistoryStore


def _write_jsonl(path: Path, role: str, content: str) -> None:
    rec = {"ts": "2025-01-01T00:00:00Z", "role": role, "content": content}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def test_us26_only_last_n_turns_loaded(tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p)

    # Write 5 turns => 10 records
    for i in range(1, 6):
        _write_jsonl(p, "user", f"u{i}")
        _write_jsonl(p, "assistant", f"a{i}")

    turns = store.load_turns(max_turns=2)

    assert [(t.user_text, t.assistant_text) for t in turns] == [
        ("u4", "a4"),
        ("u5", "a5"),
    ]


def test_us26_empty_file_returns_empty_list(tmp_path: Path) -> None:
    store = HistoryStore(path=tmp_path / "history.jsonl")
    assert store.load_turns(max_turns=3) == []
