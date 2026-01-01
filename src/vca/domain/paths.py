# src\vca\domain\paths.py
from pathlib import Path
import os

def _env_path(name: str, default: Path) -> Path:
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
INTERACTION_LOG_PATH = _env_path("VCA_INTERACTIONS_PATH", DATA_DIR / "interaction_log.jsonl")
ERROR_LOG_PATH = _env_path("VCA_ERROR_LOG_PATH", LOGS_DIR / "system_errors.log")

def ensure_runtime_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
