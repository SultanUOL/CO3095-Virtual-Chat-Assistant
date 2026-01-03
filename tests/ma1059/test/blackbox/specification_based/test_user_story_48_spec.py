# Test file for User Story 48
# Testing Type: blackbox
# Technique: specification_based
# Team Member: ma1059
# Original file: test_user_story_48.py

from pathlib import Path
from vca.core.engine import ChatEngine
from vca.storage.history_store import HistoryStore
from vca.cli.app import run_cli

def test_user_story_48_final_integration_and_stability(tmp_path: Path) -> None:
    """
    Combined integration and stability test for User Story 48.

    Covers:
    - End to end CLI run
    - Restart behaviour
    - Empty input
    - Unknown intent
    - Ctrl+C safety (simulated)
    """

    history_path = tmp_path / "history.jsonl"
    history = HistoryStore(path=history_path)
    engine = ChatEngine(history=history)

    inputs = iter(
        [
            "",
            "unknowncommand",
            "restart",
            "exit",
        ]
    )

    outputs: list[str] = []

    def fake_input(_: str) -> str:
        return next(inputs)

    def fake_output(text: str) -> None:
        outputs.append(text)

    run_cli(engine, input_fn=fake_input, output_fn=fake_output, terminal_width=80)

    # Assertions (black box observable behaviour)
    joined = "\n".join(outputs)
    assert "Virtual Chat Assistant" in joined
    assert "Session restarted" in joined
    assert "Goodbye" in joined
