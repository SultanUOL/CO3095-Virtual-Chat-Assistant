from pathlib import Path

from vca.core.engine import ChatEngine
from vca.storage.history_store import HistoryStore


def test_us42_saved_turn_exists_in_memory_with_identical_fields(tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, max_turns=10)
    engine = ChatEngine(history=store)

    engine.process_turn("hello")

    stored = store.load_turns(max_turns=1)
    assert len(stored) == 1
    assert engine.session.turns[-1] == stored[-1]


def test_us42_loading_reconstructs_same_turn_structure(tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, max_turns=10)
    store.save_turn("u1", "a1")
    store.save_turn("u2", "a2")

    expected = store.load_turns()
    engine = ChatEngine(history=store)

    assert list(engine.session.turns) == expected


def test_us42_prevents_duplicate_turns_after_load_then_continue(tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, max_turns=10)
    store.save_turn("u1", "a1")

    engine = ChatEngine(history=store)
    assert len(engine.session.turns) == 1

    engine.process_turn("u2")
    assert len(engine.session.turns) == 2


def test_us42_roundtrip_save_then_load_matches_expected_turns(tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, max_turns=10)

    engine1 = ChatEngine(history=store)
    engine1.process_turn("hello")
    engine1.process_turn("how are you")

    expected = store.load_turns()

    engine2 = ChatEngine(history=store)
    assert list(engine2.session.turns) == expected


def test_us42_trimming_consistent_between_memory_and_storage(tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"
    store = HistoryStore(path=p, max_turns=2)
    engine = ChatEngine(history=store)

    engine.process_turn("u1")
    engine.process_turn("u2")
    engine.process_turn("u3")

    assert len(store.load_turns()) == 2
    assert len(engine.session.turns) == 2
