"""
Virtual Chat Assistant
Entry point for the CLI application.
Backbone only, logic added in later sprints.
"""

from vca.cli.app import CliApp


def main() -> None:
    """Start the console application."""
    app = CliApp()
    app.run()


if __name__ == "__main__":
    main()
