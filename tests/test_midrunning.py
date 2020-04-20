from time import sleep

import pytest


@pytest.mark.parametrize("duration", [3, 3, 4, 5, 1, 5, 4, 7, 1, 1, 1, 5])
def test_passing_300seconds(duration):
    sleep(duration)
    assert True
