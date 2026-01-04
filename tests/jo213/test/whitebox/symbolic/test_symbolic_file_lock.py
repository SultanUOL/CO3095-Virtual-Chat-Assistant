"""
Symbolic Execution Tests for FileLock.try_acquire()

These tests demonstrate symbolic execution by exploring execution paths
through the FileLock.try_acquire() method.

Symbolic execution paths:
- Path 1: lock file does not exist → creates lock, returns True
- Path 2: lock file exists (valid) → returns False
- Path 3: lock file exists but error occurs → returns False
"""

import pytest
import os
from pathlib import Path
from vca.storage.file_lock import FileLock


class TestSymbolicFileLock:
    """Symbolic execution tests for FileLock.try_acquire()"""

    def test_symbolic_path_no_lock_file(self, tmp_path):
        """
        Symbolic Path 1: lock_path does not exist
        Constraint: lock file does not exist
        Expected: Creates lock file, returns True
        """
        target = tmp_path / "test_file.txt"
        lock = FileLock(target_path=target)
        
        # Lock file should not exist initially
        assert not lock.lock_path.exists()
        
        result = lock.try_acquire()
        
        assert result is True
        assert lock.lock_path.exists()

    def test_symbolic_path_lock_file_exists(self, tmp_path):
        """
        Symbolic Path 2: lock_path exists
        Constraint: lock file already exists
        Expected: Returns False (lock is busy)
        """
        target = tmp_path / "test_file.txt"
        lock = FileLock(target_path=target)
        
        # Create lock file first
        lock.try_acquire()
        assert lock.lock_path.exists()
        
        # Try to acquire again (should fail)
        result = lock.try_acquire()
        
        assert result is False

    def test_symbolic_path_lock_after_release(self, tmp_path):
        """
        Symbolic Path: lock_path exists → release → lock_path does not exist
        Tests the path where lock is released and then re-acquired
        """
        target = tmp_path / "test_file.txt"
        lock = FileLock(target_path=target)
        
        # Acquire lock
        assert lock.try_acquire() is True
        assert lock.lock_path.exists()
        
        # Release lock
        lock.release()
        assert not lock.lock_path.exists()
        
        # Should be able to acquire again
        result = lock.try_acquire()
        assert result is True
        assert lock.lock_path.exists()

    def test_symbolic_path_concurrent_acquisition(self, tmp_path):
        """
        Symbolic Path: Multiple attempts to acquire same lock
        Tests the conditional logic when lock is already held
        """
        target = tmp_path / "test_file.txt"
        lock1 = FileLock(target_path=target)
        lock2 = FileLock(target_path=target)
        
        # First lock succeeds
        assert lock1.try_acquire() is True
        
        # Second lock fails (lock exists)
        assert lock2.try_acquire() is False
        
        # Release first lock
        lock1.release()
        
        # Now second lock can acquire
        assert lock2.try_acquire() is True


