"""vca.core.settings

Application settings management.

Loads configuration from a JSON file (default: config/settings.json) with sensible
defaults. Supports overrides for history file path, history size limits, logging
level, and log file path.

Settings are loaded once at startup and used throughout the application lifecycle.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from vca.domain.constants import HISTORY_MAX_TURNS


@dataclass(frozen=True)
class Settings:
    """Immutable application configuration.
    
    Attributes:
        history_file_path: Path to the conversation history file
        history_max_turns: Maximum number of turns to keep in history (1-10000)
        log_level: Python logging level (logging.DEBUG, INFO, WARNING, etc.)
        log_file_path: Path to the error log file
    """
    history_file_path: Path
    history_max_turns: int
    log_level: int
    log_file_path: Path


DEFAULT_SETTINGS_PATH = Path("config") / "settings.json"


def load_settings(path: str | Path | None = None) -> Settings:
    """Load application settings from a JSON file.
    
    If the file doesn't exist or cannot be parsed, returns default settings.
    Default settings use standard paths and logging.WARNING level.
    
    Args:
        path: Optional path to settings file. If None, uses config/settings.json
        
    Returns:
        Settings object with loaded or default values
    """
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
    """Apply configuration overrides from a dictionary to default settings.
    
    Validates and sanitizes values, falling back to defaults for invalid entries.
    
    Args:
        defaults: Base settings to override
        obj: Dictionary of setting overrides from JSON file
        
    Returns:
        New Settings object with overrides applied
    """
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
    """Parse a path value from configuration.
    
    Args:
        value: String path or None
        default: Default Path to return if value is invalid
        
    Returns:
        Path object, or default if value cannot be converted
    """
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
    """Parse an integer within a valid range.
    
    Args:
        value: Integer value to parse
        default: Default value if parsing fails or value is out of range
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)
        
    Returns:
        Parsed integer within range, or default if invalid
    """
    try:
        num = int(value)
    except Exception:
        return int(default)
    if num < min_value or num > max_value:
        return int(default)
    return num


def _parse_log_level(value: Any, default: int) -> int:
    """Parse a logging level from string or integer.
    
    Accepts integer values directly, or string names like "DEBUG", "INFO", "WARNING".
    
    Args:
        value: Log level as integer or string name
        default: Default logging level if value cannot be parsed
        
    Returns:
        Python logging level constant (integer)
    """
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
