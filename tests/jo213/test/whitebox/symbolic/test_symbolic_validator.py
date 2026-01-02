from tests.jo213.test.whitebox.concolic.test_concolic_validator import validate_input


def vaco():
    def test_symbolic_negative():
        # Path condition: value < 0
        result = validate_input(-5)
        assert result == "NEGATIVE"


def test_symbolic_zero():
    # Path condition: value == 0
    result = validate_input(0)
    assert result == "ZERO"


def test_symbolic_small_range():
    # Path condition: 1 <= value <= 10
    result = validate_input(7)
    assert result == "SMALL"


def test_symbolic_large():
    # Path condition: value > 10
    result = validate_input(25)
    assert result == "LARGE"
