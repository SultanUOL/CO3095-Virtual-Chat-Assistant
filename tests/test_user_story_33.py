from __future__ import annotations

from types import SimpleNamespace

from vca.core.engine import ChatEngine
from vca.core.intents import Intent


def test_user_story_33_process_turn_orchestrates_stages_in_order() -> None:
    engine = ChatEngine()

    calls: list[str] = []

    def stage_validate(_raw: str | None):
        calls.append("validate")
        return SimpleNamespace(text="hello", input_length=5, was_truncated=False)

    def stage_load_context():
        calls.append("load_context")
        return []

    def stage_handle_pending(_validated, _context, _telemetry):
        calls.append("handle_pending")
        return None

    def stage_classify(_text: str, _telemetry):
        calls.append("classify")
        return Intent.UNKNOWN, None

    def stage_add_user(_text: str):
        calls.append("add_user")
        return []

    def stage_maybe_clarify(_text: str, _intent, _result, _telemetry):
        calls.append("maybe_clarify")
        return None

    def stage_generate(_text: str, _intent, _recent, _context):
        calls.append("generate")
        return "ok"

    def stage_apply_trunc(_response: str, _was_truncated: bool):
        calls.append("apply_truncation_note")
        return _response

    def stage_persist(_user_text: str, _response: str, _intent, _telemetry):
        calls.append("persist_and_return")
        return _response

    telemetry_logged = {"called": False}

    def stage_log(_telemetry):
        telemetry_logged["called"] = True
        calls.append("log_telemetry")

    engine._stage_validate = stage_validate  # type: ignore[attr-defined]
    engine._stage_load_context = stage_load_context  # type: ignore[attr-defined]
    engine._stage_handle_pending_clarification = stage_handle_pending  # type: ignore[attr-defined]
    engine._stage_classify_intent = stage_classify  # type: ignore[attr-defined]
    engine._stage_add_user_message = stage_add_user  # type: ignore[attr-defined]
    engine._stage_maybe_ask_for_clarification = stage_maybe_clarify  # type: ignore[attr-defined]
    engine._stage_generate_response = stage_generate  # type: ignore[attr-defined]
    engine._stage_apply_truncation_note = stage_apply_trunc  # type: ignore[attr-defined]
    engine._stage_persist_and_return = stage_persist  # type: ignore[attr-defined]
    engine._stage_log_telemetry = stage_log  # type: ignore[attr-defined]

    out = engine.process_turn("hello")
    assert out == "ok"
    assert telemetry_logged["called"] is True

    assert calls == [
        "validate",
        "load_context",
        "handle_pending",
        "classify",
        "add_user",
        "maybe_clarify",
        "generate",
        "apply_truncation_note",
        "persist_and_return",
        "log_telemetry",
    ]


def test_user_story_33_process_turn_logs_telemetry_even_on_exception() -> None:
    engine = ChatEngine()

    calls: list[str] = []
    telemetry_logged = {"called": False}

    def stage_validate(_raw: str | None):
        calls.append("validate")
        raise RuntimeError("boom")

    def stage_log(_telemetry):
        telemetry_logged["called"] = True
        calls.append("log_telemetry")

    engine._stage_validate = stage_validate  # type: ignore[attr-defined]
    engine._stage_log_telemetry = stage_log  # type: ignore[attr-defined]

    engine._responder.fallback_error = lambda: "fallback"  # type: ignore[assignment]

    out = engine.process_turn("hello")
    assert out == "fallback"
    assert telemetry_logged["called"] is True
    assert calls == ["validate", "log_telemetry"]


def test_user_story_33_pending_clarification_short_circuits_other_stages() -> None:
    engine = ChatEngine()

    calls: list[str] = []

    def stage_validate(_raw: str | None):
        calls.append("validate")
        return SimpleNamespace(text="1", input_length=1, was_truncated=False)

    def stage_load_context():
        calls.append("load_context")
        return []

    def stage_handle_pending(_validated, _context, _telemetry):
        calls.append("handle_pending")
        return "clarified"

    telemetry_logged = {"called": False}

    def stage_log(_telemetry):
        telemetry_logged["called"] = True
        calls.append("log_telemetry")

    engine._stage_validate = stage_validate  # type: ignore[attr-defined]
    engine._stage_load_context = stage_load_context  # type: ignore[attr-defined]
    engine._stage_handle_pending_clarification = stage_handle_pending  # type: ignore[attr-defined]
    engine._stage_log_telemetry = stage_log  # type: ignore[attr-defined]

    out = engine.process_turn("1")
    assert out == "clarified"
    assert telemetry_logged["called"] is True

    assert calls == [
        "validate",
        "load_context",
        "handle_pending",
        "log_telemetry",
    ]
