"""
CLI layer for the Virtual Chat Assistant.
Handles input and output only.
"""

from vca.core.engine import ChatEngine


class CliApp:
    """Console application wrapper."""

    def __init__(self) -> None:
        self._engine = ChatEngine()

    def run(self) -> None:
        """
        Main conversation loop.
        Skeleton now, implemented in Sprint 1.
        """
        raise NotImplementedError("Sprint 1 will implement the CLI loop.")
