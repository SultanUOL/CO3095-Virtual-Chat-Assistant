# src/vca/main.py
from __future__ import annotations

from vca.cli.app import CliApp
from vca.core.engine import ChatEngine
from vca.core.logging_config import configure_logging
from vca.core.settings import load_settings
from vca.storage.history_store import HistoryStore


def main() -> None:
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


if __name__ == "__main__":
    main()