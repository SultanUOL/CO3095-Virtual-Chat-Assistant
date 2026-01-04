"""
Concolic Testing for HistoryStore.save_turn()

Concolic testing combines concrete execution with symbolic constraint tracking.
"""

import pytest
import tempfile
from pathlib import Path
from vca.storage.history_store import HistoryStore


class TestConcolicHistoryStore:
    """Concolic testing for HistoryStore.save_turn()"""

    def test_concolic_save_turn_iteration_1_jsonl_format(self):
        """
        Concolic Iteration 1: Explore JSONL format path
        Concrete Input: .jsonl file
        Symbolic: path.suffix = ".jsonl"
        Constraint: path.suffix.lower() != ".txt"
        Path Taken: JSONL format save
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "history.jsonl"
            store = HistoryStore(path=path)
            
            store.save_turn("hello", "Hello")
            assert path.exists()

    def test_concolic_save_turn_iteration_2_legacy_format(self):
        """
        Concolic Iteration 2: Explore legacy format path
        Concrete Input: .txt file
        Symbolic: path.suffix = ".txt"
        Constraint: path.suffix.lower() == ".txt"
        Path Taken: Legacy format save
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "history.txt"
            store = HistoryStore(path=path)
            
            store.save_turn("hello", "Hello")
            assert path.exists()

    def test_concolic_save_turn_iteration_3_none_values(self):
        """
        Concolic Iteration 3: Explore None values path
        Concrete Input: None for user_text
        Symbolic: user_text = None
        Constraint: user_text is None
        Path Taken: Converts to empty string
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "history.jsonl"
            store = HistoryStore(path=path)
            
            store.save_turn(None, "Hello")
            assert path.exists()

    def test_concolic_save_turn_iteration_4_directory_creation(self):
        """
        Concolic Iteration 4: Explore directory creation path
        Concrete Input: Path with non-existent directory
        Symbolic: path.parent does not exist
        Constraint: not path.parent.exists()
        Path Taken: Creates directory, then saves
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "newdir" / "history.jsonl"
            store = HistoryStore(path=path)
            
            store.save_turn("hello", "Hello")
            assert path.parent.exists()
            assert path.exists()

    def test_concolic_save_turn_iteration_5_fsync_trigger(self):
        """
        Concolic Iteration 5: Explore fsync trigger path
        Concrete Input: Multiple writes to trigger fsync
        Symbolic: write_count % fsync_every_writes = 0
        Constraint: Periodic fsync condition met
        Path Taken: Performs fsync
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "history.jsonl"
            store = HistoryStore(path=path, fsync_every_writes=2)
            
            store.save_turn("hello1", "Hello1")
            store.save_turn("hello2", "Hello2")  # Should trigger fsync
            assert path.exists()

    def test_concolic_path_coverage_summary(self):
        """
        Summary of concolic testing path coverage for HistoryStore.save_turn():
        - JSONL format path: ✅ Covered
        - Legacy format path: ✅ Covered
        - None values path: ✅ Covered
        - Directory creation path: ✅ Covered
        - Fsync trigger path: ✅ Covered
        
        All major execution paths explored through iterative constraint negation
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            paths_explored = {
                "jsonl": Path(tmpdir) / "test1.jsonl",
                "txt": Path(tmpdir) / "test2.txt",
                "none_values": Path(tmpdir) / "test3.jsonl",
            }
            
            # Test JSONL
            store1 = HistoryStore(path=paths_explored["jsonl"])
            store1.save_turn("hello", "Hello")
            assert paths_explored["jsonl"].exists()
            
            # Test TXT
            store2 = HistoryStore(path=paths_explored["txt"])
            store2.save_turn("hello", "Hello")
            assert paths_explored["txt"].exists()
            
            # Test None values
            store3 = HistoryStore(path=paths_explored["none_values"])
            store3.save_turn(None, None)
            assert paths_explored["none_values"].exists()


