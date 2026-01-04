# Test file for User Story 36
# Testing Type: blackbox
# Technique: random_based
# Team Member: sa1068
# Original file: test_user_story_36.py


from __future__ import annotations
from helpers import FakeHistory, FakeInteractionLog
from vca.cli.app import CliApp, run_cli
from vca.core.engine import ChatEngine


def test_user_story_36_cli_can_be_tested_without_real_io() -> None:
    history = FakeHistory()
    log = FakeInteractionLog()
    engine = ChatEngine(history=history, interaction_log=log)

    inputs = iter(["help", "exit"])
    outputs: list[str] = []

    def input_fn(_prompt: str) -> str:
        return next(inputs)

    def output_fn(text: str) -> None:
        outputs.append(text)

    app = CliApp(engine=engine)
    app.run_with_io(input_fn=input_fn, output_fn=output_fn, terminal_width=80)

    assert any("Virtual Chat Assistant" in s for s in outputs)
    assert any("Assistant:" in s for s in outputs)


def test_user_story_36_run_cli_wrapper_is_available() -> None:
    history = FakeHistory()
    log = FakeInteractionLog()
    engine = ChatEngine(history=history, interaction_log=log)

    inputs = iter(["exit"])
    outputs: list[str] = []

    def input_fn(_prompt: str) -> str:
        return next(inputs)

    def output_fn(text: str) -> None:
        outputs.append(text)

    run_cli(engine, input_fn=input_fn, output_fn=output_fn, terminal_width=80)
    assert any("Virtual Chat Assistant" in s for s in outputs)
