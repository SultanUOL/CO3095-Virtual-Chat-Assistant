# Test file for User Story 29
# Testing Type: whitebox
# Technique: statement_coverage
# Team Member: ma1059
# Original file: test_user_story_29.py

from __future__ import annotations
import logging
from pathlib import Path
from vca.core.logging_config import configure_logging


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
