"""vca.domain.paths

Runtime path configuration for the Virtual Chat Assistant.

Provides centralized path definitions for data directories, log files, and history storage.
Paths can be overridden using environment variables:
- VCA_DATA_DIR: Override the data directory
- VCA_LOGS_DIR: Override the logs directory
- VCA_HISTORY_PATH: Override the history file path
- VCA_INTERACTIONS_PATH: Override the interaction log path
- VCA_ERROR_LOG_PATH: Override the error log path
"""

from pathlib import Path
import os


def _env_path(name: str, default: Path) -> Path:
    """Read a path from an environment variable or return the default.
    
    Args:
        name: Environment variable name to read
        default: Default Path to return if the variable is not set or empty
        
    Returns:
        Path from environment variable if set and non-empty, otherwise default
    """
    raw = os.getenv(name)
    if raw is None:
        return default
    raw = raw.strip()
    if not raw:
        return default
    return Path(raw)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = _env_path("VCA_DATA_DIR", PROJECT_ROOT / "data")
LOGS_DIR = _env_path("VCA_LOGS_DIR", PROJECT_ROOT / "logs")

HISTORY_PATH = _env_path("VCA_HISTORY_PATH", DATA_DIR / "history.jsonl")
INTERACTION_LOG_PATH = _env_path(
    "VCA_INTERACTIONS_PATH", DATA_DIR / "interaction_log.jsonl"
)
ERROR_LOG_PATH = _env_path("VCA_ERROR_LOG_PATH", LOGS_DIR / "system_errors.log")


def ensure_runtime_dirs() -> None:
    """Ensure that required runtime directories (data and logs) exist.
    
    Creates the directories if they don't exist, including parent directories.
    Safe to call multiple times (idempotent).
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
