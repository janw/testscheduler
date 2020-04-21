from time import sleep


def test_failing():
    assert False


def test_failing_long():
    sleep(45)
    assert False
