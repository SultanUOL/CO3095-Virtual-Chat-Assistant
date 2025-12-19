import logging
from pathlib import Path

from vca.core.engine import ChatEngine
from vca.core.logging_config import configure_logging
from vca.storage.history_store import HistoryStore


def test_exception_logged_to_file_without_console_traceback(tmp_path: Path, capsys) -> None:
    log_path = tmp_path / "system_errors.log"
    configure_logging(log_file_path=log_path, force=True, console_level=logging.ERROR)

    engine = ChatEngine(history=HistoryStore(path=tmp_path / "history.txt"))

    def boom(_text: str, _recent: list) -> str:
        raise ZeroDivisionError("forced")

    engine.route_intent = lambda _intent: boom

    reply = engine.process_turn("hello")
    assert isinstance(reply, str)

    captured = capsys.readouterr()
    combined = (captured.out or "") + (captured.err or "")
    assert "Traceback" not in combined

    text = log_path.read_text(encoding="utf-8")
    assert "ERROR" in text
    assert "error_type=ZeroDivisionError" in text


def test_logging_still_works_when_history_cannot_be_written(tmp_path: Path) -> None:
    log_path = tmp_path / "system_errors.log"
    configure_logging(log_file_path=log_path, force=True, console_level=logging.ERROR)


    history_dir = tmp_path / "history_dir"
    history_dir.mkdir(parents=True, exist_ok=True)

    engine = ChatEngine(history=HistoryStore(path=history_dir))

    reply = engine.process_turn("hello")
    assert isinstance(reply, str)

    text = log_path.read_text(encoding="utf-8")
    assert "History save failed" in text
