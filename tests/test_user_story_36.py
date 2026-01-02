from __future__ import annotations


from vca.cli.app import CliApp, run_cli
from vca.core.engine import ChatEngine
from vca.core.intents import Intent


class FakeHistory:
    def __init__(self) -> None:
        self.saved: list[tuple[str, str]] = []
        self.cleared = False
        self.flushed = False
        self.closed = False

    def load_turns(self, max_turns=None):
        return []

    def save_turn(self, user_text: str, assistant_text: str) -> None:
        self.saved.append((user_text, assistant_text))

    def clear_file(self) -> None:
        self.cleared = True

    def flush(self) -> None:
        self.flushed = True

    def close(self) -> None:
        self.closed = True


class FakeInteractionLog:
    def __init__(self) -> None:
        self.events: list[dict] = []
        self.flushed = False
        self.closed = False

    def append_event(
        self,
        input_length: int,
        intent,
        fallback_used: bool,
        confidence: float = 0.0,
        processing_time_ms: int = 0,
        rule_match_count: int = 0,
        multiple_rules_matched: bool = False,
    ) -> None:
        self.events.append(
            {
                "input_length": input_length,
                "intent": str(intent.value)
                if hasattr(intent, "value")
                else str(intent),
                "fallback_used": bool(fallback_used),
                "confidence": float(confidence),
                "processing_time_ms": int(processing_time_ms),
                "rule_match_count": int(rule_match_count),
                "multiple_rules_matched": bool(multiple_rules_matched),
            }
        )

    def flush(self) -> None:
        self.flushed = True

    def close(self) -> None:
        self.closed = True


class SeqClock:
    def __init__(self, values: list[float]) -> None:
        self._values = list(values)
        self._i = 0

    def __call__(self) -> float:
        if self._i >= len(self._values):
            return self._values[-1]
        v = self._values[self._i]
        self._i += 1
        return v


def test_user_story_36_engine_allows_injected_storage_and_clock(monkeypatch) -> None:
    history = FakeHistory()
    log = FakeInteractionLog()
    clock = SeqClock([10.0, 10.123])

    engine = ChatEngine(history=history, interaction_log=log, perf_counter=clock)

    def fixed_intent(_text: str):
        return Intent.HELP

    monkeypatch.setattr(engine, "classify_intent", fixed_intent, raising=True)

    reply = engine.process_turn("help")
    assert isinstance(reply, str)

    assert len(history.saved) == 1
    assert history.saved[0][0] == "help"

    assert len(log.events) == 1
    assert log.events[0]["processing_time_ms"] == 123


def test_user_story_36_engine_uses_safe_fallback_on_processing_error(
    monkeypatch,
) -> None:
    history = FakeHistory()
    log = FakeInteractionLog()
    clock = SeqClock([1.0, 1.01])

    engine = ChatEngine(history=history, interaction_log=log, perf_counter=clock)

    def boom(_text: str, _recent, _context):
        raise RuntimeError("forced")

    monkeypatch.setattr(engine, "route_intent", lambda _intent: boom, raising=True)

    reply = engine.process_turn("hello")
    assert isinstance(reply, str)

    assert len(log.events) == 1
    assert log.events[0]["fallback_used"] is True


def test_user_story_36_cli_can_be_tested_without_real_io() -> None:
    history = FakeHistory()
    log = FakeInteractionLog()
    engine = ChatEngine(history=history, interaction_log=log)

    inputs = iter(["help", "exit"])
    outputs: list[str] = []

    def input_fn(_prompt: str) -> str:
        return next(inputs)

    def output_fn(text: str) -> None:
        outputs.append(text)

    app = CliApp(engine=engine)
    app.run_with_io(input_fn=input_fn, output_fn=output_fn, terminal_width=80)

    assert any("Virtual Chat Assistant" in s for s in outputs)
    assert any("Assistant:" in s for s in outputs)


def test_user_story_36_run_cli_wrapper_is_available() -> None:
    history = FakeHistory()
    log = FakeInteractionLog()
    engine = ChatEngine(history=history, interaction_log=log)

    inputs = iter(["exit"])
    outputs: list[str] = []

    def input_fn(_prompt: str) -> str:
        return next(inputs)

    def output_fn(text: str) -> None:
        outputs.append(text)

    run_cli(engine, input_fn=input_fn, output_fn=output_fn, terminal_width=80)
    assert any("Virtual Chat Assistant" in s for s in outputs)
