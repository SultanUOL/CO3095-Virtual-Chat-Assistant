from vca.core.engine import ChatEngine
from vca.core.validator import InputValidator


def test_us19_whitespace_only_input_becomes_empty() -> None:
    v = InputValidator()
    out = v.clean("   \t\n  ")
    assert out.text == ""
    assert out.was_truncated is False


def test_us19_extremely_long_input_is_truncated_by_rule() -> None:
    v = InputValidator()
    raw = "x" * (v.MAX_LEN + 123)
    out = v.clean(raw)
    assert len(out.text) == v.MAX_LEN
    assert out.was_truncated is True


def test_us19_repeated_punctuation_is_collapsed_deterministically() -> None:
    v = InputValidator()
    out = v.clean("wow!!!!!! really???? ...")
    assert "!!!!!!" not in out.text
    assert "????" not in out.text
    assert "!!!" in out.text
    assert "???" in out.text


def test_us19_emoji_is_preserved_and_does_not_crash() -> None:
    e = ChatEngine()
    reply = e.process_turn("😄😄😄!!!\n\tokay")
    assert isinstance(reply, str)


def test_us19_tabs_and_newlines_are_normalised_to_spaces() -> None:
    v = InputValidator()
    out = v.clean("hello\tworld\nnew\rline")
    assert out.text == "hello world new line"
