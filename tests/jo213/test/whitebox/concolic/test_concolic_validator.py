import pytest

def validate_input(value: int) -> str:
    if value < 0:
        return "NEGATIVE"
    elif value == 0:
        return "ZERO"
    elif 1 <= value <= 10:
        return "SMALL"
    else:
        return "LARGE"


def test_concolic_execution():
    """
    Concolic testing approach:
    Start with concrete input, observe path, negate predicate.
    """

    # Initial concrete execution
    seed = 5
    assert validate_input(seed) == "SMALL"

    # Negated predicate: value <= 0
    assert validate_input(0) == "ZERO"
    assert validate_input(-3) == "NEGATIVE"

    # Negated predicate: value > 10
    assert validate_input(20) == "LARGE"
