def validate_input(value: int) -> str:
    """
    Example validation logic already present in the system.
    Used here for symbolic execution analysis.
    """
    if value < 0:
        return "NEGATIVE"
    elif value == 0:
        return "ZERO"
    elif 1 <= value <= 10:
        return "SMALL"
    else:
        return "LARGE"


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
