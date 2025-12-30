from __future__ import annotations

from pathlib import Path

from vca.cli.app import CliApp
from vca.core.engine import ChatEngine
from vca.storage.history_store import HistoryStore


def test_user_story_34_engine_returns_safe_fallback_on_unhandled_exception(monkeypatch) -> None:
    engine = ChatEngine()
    engine._responder.fallback_error = lambda: "fallback"  # type: ignore[assignment]

    def boom(_raw):
        raise RuntimeError("boom")

    monkeypatch.setattr(engine, "_stage_validate", boom)

    out = engine.process_turn("hello")
    assert out == "fallback"


def test_user_story_34_history_store_does_not_crash_on_save_open_error(monkeypatch, tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.jsonl")

    def bad_open(*args, **kwargs):
        raise OSError("disk error")

    monkeypatch.setattr(Path, "open", bad_open, raising=True)

    store.save_turn("hi", "hello")


def test_user_story_34_history_store_does_not_crash_on_load_open_error(monkeypatch, tmp_path: Path) -> None:
    p = tmp_path / "history.jsonl"
    p.write_text('{"ts":"x","role":"user","content":"a"}\n', encoding="utf-8")
    store = HistoryStore(p)

    def bad_open(*args, **kwargs):
        raise OSError("read error")

    monkeypatch.setattr(Path, "open", bad_open, raising=True)

    turns = store.load_turns()
    assert turns == []


def test_user_story_34_cli_handles_keyboard_interrupt() -> None:
    engine = ChatEngine()
    app = CliApp(engine=engine)

    def input_fn(_prompt: str) -> str:
        raise KeyboardInterrupt

    outputs: list[str] = []

    def output_fn(s: str) -> None:
        outputs.append(s)

    app.run_with_io(input_fn=input_fn, output_fn=output_fn, terminal_width=80)

    combined = "\n".join(outputs).lower()
    assert "goodbye" in combined


def test_user_story_34_cli_handles_eof() -> None:
    engine = ChatEngine()
    app = CliApp(engine=engine)

    def input_fn(_prompt: str) -> str:
        raise EOFError

    outputs: list[str] = []

    def output_fn(s: str) -> None:
        outputs.append(s)

    app.run_with_io(input_fn=input_fn, output_fn=output_fn, terminal_width=80)

    combined = "\n".join(outputs).lower()
    assert "goodbye" in combined


def test_user_story_34_cli_recovers_from_input_error() -> None:
    engine = ChatEngine()
    app = CliApp(engine=engine)

    calls = {"n": 0}

    def input_fn(_prompt: str) -> str:
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("weird input failure")
        return "exit"

    outputs: list[str] = []

    def output_fn(s: str) -> None:
        outputs.append(s)

    app.run_with_io(input_fn=input_fn, output_fn=output_fn, terminal_width=80)

    combined = "\n".join(outputs).lower()
    assert "input error" in combined or "goodbye" in combined
