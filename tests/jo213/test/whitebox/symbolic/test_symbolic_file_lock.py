def acquire_lock(is_locked: bool, user_is_owner: bool) -> bool:
    """
    Simplified file lock logic reflecting branching behaviour.
    """
    if not is_locked:
        return True
    elif is_locked and user_is_owner:
        return True
    else:
        return False


def test_symbolic_lock_free():
    # Path condition: not is_locked
    assert acquire_lock(False, False) is True


def test_symbolic_lock_owner():
    # Path condition: is_locked and user_is_owner
    assert acquire_lock(True, True) is True


def test_symbolic_lock_denied():
    # Path condition: is_locked and not user_is_owner
    assert acquire_lock(True, False) is False
