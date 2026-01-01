# src/vca/main.py
from __future__ import annotations

import logging

from vca.cli.app import CliApp
from vca.core.engine import ChatEngine
from vca.core.logging_config import configure_logging
from vca.core.settings import load_settings
from vca.domain.paths import (
    ensure_runtime_dirs,
    ERROR_LOG_PATH,
    HISTORY_PATH,
)
from vca.storage.history_store import HistoryStore

logger = logging.getLogger(__name__)
error_logger = logging.getLogger("vca.errors")


def main() -> None:
    """
    Startup sequence
    1 ensure runtime directories exist
    2 load settings
    3 configure logging
    4 initialise storage
    5 initialise engine
    6 run cli

    Failures during startup are handled safely with
    1 clear user message
    2 error log entry
    """
    try:
        # 1 ensure runtime folders exist
        ensure_runtime_dirs()

        # 2 load settings
        settings = load_settings()

        # 3 configure logging
        configure_logging(
            log_file_path=settings.log_file_path or ERROR_LOG_PATH,
            console_level=settings.log_level,
            file_level=settings.log_level,
            force=True,
        )

        # 4 initialise storage
        history = HistoryStore(
            path=settings.history_file_path or HISTORY_PATH,
            max_turns=settings.history_max_turns,
        )

        # 5 initialise engine
        engine = ChatEngine(history=history)

        # 6 run cli
        app = CliApp(engine=engine)
        app.run()

    except Exception as ex:
        try:
            error_logger.exception(
                "Startup failed error_type=%s",
                type(ex).__name__,
            )
        except Exception:
            pass

        # User safe message
        try:
            print("Assistant: Startup failed. Please check logs and try again.")
        except Exception:
            pass


if __name__ == "__main__":
    main()