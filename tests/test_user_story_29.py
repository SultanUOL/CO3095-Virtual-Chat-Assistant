from __future__ import annotations

import json
import logging
from pathlib import Path

from vca.core.settings import load_settings
from vca.domain.constants import HISTORY_MAX_TURNS
from vca.core.engine import ChatEngine
from vca.core.logging_config import configure_logging
from vca.storage.history_store import HistoryStore


def test_configured_history_path_and_limit_affect_loaded_turns(tmp_path: Path) -> None:
    history_path = tmp_path / "history.jsonl"

    lines: list[str] = []
    for i in range(6):
        lines.append(json.dumps({"role": "user", "content": f"u{i}"}))
        lines.append(json.dumps({"role": "assistant", "content": f"a{i}"}))
    history_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    store = HistoryStore(path=history_path, max_turns=3)
    engine = ChatEngine(history=store)

    assert engine.loaded_turns_count == 3


def test_configured_log_file_path_receives_logs(tmp_path: Path) -> None:
    log_path = tmp_path / "system_errors.log"

    configure_logging(
        log_file_path=log_path,
        console_level=logging.CRITICAL,
        file_level=logging.INFO,
        force=True,
    )

    logger = logging.getLogger("vca.us29.blackbox")
    logger.info("settings log check")

    for handler in logging.getLogger().handlers:
        try:
            handler.flush()
        except Exception:
            pass

    assert log_path.exists()
    assert "settings log check" in log_path.read_text(encoding="utf-8")


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