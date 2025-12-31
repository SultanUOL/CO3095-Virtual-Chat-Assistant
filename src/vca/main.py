# src/vca/main.py
from __future__ import annotations

import logging

from vca.cli.app import CliApp
from vca.core.engine import ChatEngine
from vca.core.logging_config import configure_logging
from vca.core.settings import load_settings
from vca.storage.history_store import HistoryStore

logger = logging.getLogger(__name__)
error_logger = logging.getLogger("vca.errors")


def main() -> None:
    """
    Startup sequence is always
    1 load settings
    2 configure logging
    3 initialise storage
    4 initialise engine
    5 run cli

    Failures during startup are handled safely with
    1 clear user message
    2 error log entry
    """
    try:
        settings = load_settings()

        configure_logging(
            log_file_path=settings.log_file_path,
            console_level=settings.log_level,
            file_level=settings.log_level,
            force=True,
        )

        history = HistoryStore(path=settings.history_file_path, max_turns=settings.history_max_turns)
        engine = ChatEngine(history=history)

        app = CliApp(engine=engine)
        app.run()

    except Exception as ex:
        try:
            error_logger.exception("Startup failed error_type=%s", type(ex).__name__)
        except Exception:
            pass

        # User safe message
        try:
            print("Assistant: Startup failed. Please check logs and try again.")
        except Exception:
            pass


if __name__ == "__main__":
    main()
