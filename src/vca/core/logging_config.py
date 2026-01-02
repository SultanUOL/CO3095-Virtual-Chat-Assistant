from __future__ import annotations

import logging
import sys
from pathlib import Path


class _SafeConsoleFormatter(logging.Formatter):
    """Formatter that suppresses exception tracebacks in console output."""

    def formatException(self, ei) -> str:  # noqa: N802
        return ""

    def format(self, record: logging.LogRecord) -> str:
        return super().format(record).rstrip()


class _StripExceptionInfoFilter(logging.Filter):
    """Filter that removes exception details from console records."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.exc_info = None
        record.exc_text = None
        return True


def configure_logging(
    log_file_path: str | Path | None = None,
    *,
    console_level: int = logging.WARNING,
    file_level: int = logging.WARNING,
    force: bool = False,
) -> None:
    """Configure application logging.

    Errors are written to a file for diagnosis.
    Console output stays safe by suppressing stack traces.
    """
    root = logging.getLogger()

    if root.handlers and not force:
        return

    if force:
        for h in list(root.handlers):
            root.removeHandler(h)
            try:
                h.close()
            except Exception:
                pass

    root.setLevel(logging.DEBUG)

    log_file = (
        Path(log_file_path)
        if log_file_path is not None
        else Path("logs") / "system_errors.log"
    )
    log_file.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )

    console_handler = logging.StreamHandler(stream=sys.stderr)
    console_handler.setLevel(console_level)
    console_handler.addFilter(_StripExceptionInfoFilter())
    console_handler.setFormatter(
        _SafeConsoleFormatter("%(levelname)s %(name)s %(message)s")
    )

    root.addHandler(file_handler)
    root.addHandler(console_handler)
