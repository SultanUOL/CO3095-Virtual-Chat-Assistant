# src/vca/core/settings.py
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from vca.domain.constants import HISTORY_MAX_TURNS


@dataclass(frozen=True)
class Settings:
    history_file_path: Path
    history_max_turns: int
    log_level: int
    log_file_path: Path


DEFAULT_SETTINGS_PATH = Path("config") / "settings.json"


def load_settings(path: str | Path | None = None) -> Settings:
    settings_path = Path(path) if path is not None else DEFAULT_SETTINGS_PATH

    defaults = Settings(
        history_file_path=Path("data") / "history.jsonl",
        history_max_turns=int(HISTORY_MAX_TURNS),
        log_level=logging.WARNING,
        log_file_path=Path("logs") / "system_errors.log",
    )

    try:
        raw_text = settings_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return defaults
    except Exception:
        return defaults

    try:
        obj = json.loads(raw_text)
    except Exception:
        return defaults

    if not isinstance(obj, Mapping):
        return defaults

    return _apply_overrides(defaults, obj)


def _apply_overrides(defaults: Settings, obj: Mapping[str, Any]) -> Settings:
    history_file_path = _parse_path(
        obj.get("history_file_path"), defaults.history_file_path
    )
    history_max_turns = _parse_int_range(
        obj.get("history_max_turns"),
        default=defaults.history_max_turns,
        min_value=1,
        max_value=10000,
    )
    log_level = _parse_log_level(obj.get("log_level"), defaults.log_level)
    log_file_path = _parse_path(obj.get("log_file_path"), defaults.log_file_path)

    return Settings(
        history_file_path=history_file_path,
        history_max_turns=history_max_turns,
        log_level=log_level,
        log_file_path=log_file_path,
    )


def _parse_path(value: Any, default: Path) -> Path:
    if value is None:
        return default
    if not isinstance(value, str):
        return default
    text = value.strip()
    if not text:
        return default
    try:
        return Path(text)
    except Exception:
        return default


def _parse_int_range(
    value: Any, *, default: int, min_value: int, max_value: int
) -> int:
    try:
        num = int(value)
    except Exception:
        return int(default)
    if num < min_value or num > max_value:
        return int(default)
    return num


def _parse_log_level(value: Any, default: int) -> int:
    if value is None:
        return int(default)

    if isinstance(value, int):
        return value

    if not isinstance(value, str):
        return int(default)

    name = value.strip().upper()
    if not name:
        return int(default)

    mapping = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }
    return mapping.get(name, int(default))
