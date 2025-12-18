from __future__ import annotations

import logging


def configure_logging() -> None:
    """
    Configure application logging.

    By default, this is quiet on the console because level is WARNING.
    Debug information is still available by changing the level in code or via IDE.
    """
    root = logging.getLogger()
    if root.handlers:
        return

    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
