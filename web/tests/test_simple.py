from time import sleep

import pytest


def test_passing():
    assert True


@pytest.mark.parametrize("delay", [0.1, 0.4, 0.1, 0.1, 0.9, 0.2])
def test_parametrized_delayed(delay):
    sleep(delay)
    assert True
