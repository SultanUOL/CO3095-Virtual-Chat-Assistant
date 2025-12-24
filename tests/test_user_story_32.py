from __future__ import annotations

from pathlib import Path

import pytest

from vca.cli.app import CliApp
from vca.core.engine import ChatEngine
from vca.storage.history_store import HistoryStore
from vca.storage.interaction_log_store import InteractionLogStore


def test_us32_exit_command_calls_shutdown_and_exits_cleanly() -> None:
    class FakeEngine:
        def __init__(self) -> None:
            self.shutdown_called = 0

        def shutdown(self) -> None:
            self.shutdown_called += 1

        loaded_turns_count = 0

    engine = FakeEngine()
    app = CliApp(engine=engine)

    inputs = iter(["exit"])
    outputs: list[str] = []

    def input_fn(_prompt: str) -> str:
        return next(inputs)

    def output_fn(msg: str) -> None:
        outputs.append(msg)

    app.run_with_io(input_fn=input_fn, output_fn=output_fn)

    assert engine.shutdown_called == 1
    assert any("Goodbye" in line for line in outputs)


def test_us32_ctrl_c_calls_shutdown_and_does_not_raise() -> None:
    class FakeEngine:
        def __init__(self) -> None:
            self.shutdown_called = 0

        def shutdown(self) -> None:
            self.shutdown_called += 1

        loaded_turns_count = 0

    engine = FakeEngine()
    app = CliApp(engine=engine)

    outputs: list[str] = []

    def input_fn(_prompt: str) -> str:
        raise KeyboardInterrupt()

    def output_fn(msg: str) -> None:
        outputs.append(msg)

    app.run_with_io(input_fn=input_fn, output_fn=output_fn)

    assert engine.shutdown_called == 1
    assert any("Goodbye" in line for line in outputs)


def test_us32_engine_shutdown_is_safe_and_history_is_not_corrupted(tmp_path: Path) -> None:
    history_path = tmp_path / "history.jsonl"
    interaction_path = tmp_path / "interaction_log.jsonl"

    engine = ChatEngine(
        history=HistoryStore(path=history_path),
        interaction_log=InteractionLogStore(path=interaction_path),
    )

    _ = engine.process_turn("hi")
    engine.shutdown()

    text = history_path.read_text(encoding="utf-8").strip()
    assert text != ""
    for line in text.splitlines():
        assert line.startswith("{") and line.endswith("}")