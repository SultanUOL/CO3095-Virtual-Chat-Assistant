from pathlib import Path
from vca.core.engine import ChatEngine
from vca.storage.history_store import HistoryStore

def test_history_loaded_on_startup(tmp_path: Path):
    p = tmp_path / "history.txt"
    p.write_text(
        "USER: hi\nASSISTANT: hello\n---\n",
        encoding="utf-8"
    )

    engine = ChatEngine(history=HistoryStore(path=p))
    assert engine.loaded_turns_count == 1

def test_missing_history_file_starts_empty(tmp_path: Path):
    engine = ChatEngine(history=HistoryStore(path=tmp_path / "missing.txt"))
    assert engine.loaded_turns_count == 0
