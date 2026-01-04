# Test file for User Story 32
# Testing Type: blackbox
# Technique: random_based
# Team Member: ma1059
# Original file: test_user_story_32.py

from __future__ import annotations
from vca.cli.app import CliApp


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
