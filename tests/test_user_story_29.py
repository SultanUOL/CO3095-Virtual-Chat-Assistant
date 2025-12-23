from __future__ import annotations

import json
import logging
from pathlib import Path

from vca.core.settings import load_settings
from vca.domain.constants import HISTORY_MAX_TURNS


def test_settings_missing_file_uses_safe_defaults(tmp_path: Path) -> None:
    settings = load_settings(tmp_path / "missing.json")

    assert settings.history_file_path.as_posix().endswith("data/history.jsonl")
    assert settings.history_max_turns == HISTORY_MAX_TURNS
    assert settings.log_level == logging.WARNING
    assert settings.log_file_path.as_posix().endswith("data/system_errors.log")


def test_settings_valid_file_overrides_defaults(tmp_path: Path) -> None:
    p = tmp_path / "settings.json"
    p.write_text(
        json.dumps(
            {
                "history_file_path": "data/custom_history.jsonl",
                "history_max_turns": 7,
                "log_level": "INFO",
                "log_file_path": "data/custom_errors.log",
            }
        ),
        encoding="utf-8",
    )

    settings = load_settings(p)

    assert settings.history_file_path.as_posix().endswith("data/custom_history.jsonl")
    assert settings.history_max_turns == 7
    assert settings.log_level == logging.INFO
    assert settings.log_file_path.as_posix().endswith("data/custom_errors.log")


def test_settings_invalid_values_fall_back_per_field(tmp_path: Path) -> None:
    p = tmp_path / "settings.json"
    p.write_text(
        json.dumps(
            {
                "history_file_path": "",
                "history_max_turns": "nope",
                "log_level": "LOUD",
            }
        ),
        encoding="utf-8",
    )

    settings = load_settings(p)

    assert settings.history_file_path.as_posix().endswith("data/history.jsonl")
    assert settings.history_max_turns == HISTORY_MAX_TURNS
    assert settings.log_level == logging.WARNING