"""
Virtual Chat Assistant
Entry point for the CLI application.
"""
from __future__ import annotations

from vca.cli.app import CliApp
from vca.core.logging_config import configure_logging


def main() -> None:
    """Start the console application."""
    configure_logging()
    app = CliApp()
    app.run()


if __name__ == "__main__":
    main()
