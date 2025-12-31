from __future__ import annotations

import os
import time
import logging
from dataclasses import dataclass
from pathlib import Path


logger = logging.getLogger(__name__)


class FileLockTimeout(Exception):
    """Raised when a file lock cannot be acquired within retry budget."""


@dataclass
class FileLock:
    """
    Simple cross-platform lock using a lockfile (path + '.lock').

    Assumptions/limits:
    - Best-effort mutual exclusion between processes/threads using the same lock strategy.
    - If a process crashes while holding the lock, the lockfile may remain (stale).
      This project treats that as "locked" and fails safely (logged warning).
    """

    target_path: Path
    retries: int = 3
    delay_s: float = 0.01

    @property
    def lock_path(self) -> Path:
        return Path(str(self.target_path) + ".lock")

    def try_acquire(self) -> bool:
        """Non-raising acquire attempt used for reads (return False if locked)."""
        try:
            fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            try:
                os.write(fd, str(os.getpid()).encode("utf-8"))
            finally:
                os.close(fd)
            return True
        except FileExistsError:
            return False
        except Exception:
            return False

    def acquire(self) -> None:
        """Acquire lock with retries, else raise FileLockTimeout."""
        attempts = max(1, int(self.retries))
        for i in range(attempts):
            if self.try_acquire():
                return
            if i < attempts - 1:
                time.sleep(max(0.0, float(self.delay_s)))
        raise FileLockTimeout(f"Lock busy: {self.lock_path}")

    def release(self) -> None:
        try:
            if self.lock_path.exists():
                self.lock_path.unlink()
        except Exception:
            # non-fatal
            return

    def __enter__(self) -> "FileLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()
