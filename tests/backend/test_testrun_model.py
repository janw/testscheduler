

def test_testrun_model_repr():
    """Test the __repr__ method to include the run's ID and Env ID."""
    from testscheduler.models import TestRun

    tr = TestRun()
    assert "TestRun" in repr(tr)

    tr.id = 42
    tr.env_id = 78

    assert "TestRun 42" in repr(tr)
    assert "Env 78" in repr(tr)
