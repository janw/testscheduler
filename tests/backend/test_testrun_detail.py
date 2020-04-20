import pytest


def test_testrun_details(client):
    """Tests the testruns endpoint to create a new run.

    A new test run will be created and expected to match the output of the
    next GET to the same endpoint (as first list item).
    """
    json = {"username": "John", "env_id": 1, "path": "./"}
    expected_fields = {**json, "id": 1, "logs": False, "status": "created"}

    ret = client.post("/api/testruns", json=json)
    assert ret.status_code == 201
    json_post = ret.get_json()

    entry_id = json_post["id"]
    ret = client.get(f"/api/testruns/{entry_id}")
    assert ret.status_code == 200
    data = ret.get_json()
    for field, value in expected_fields.items():
        assert field in data
        assert data[field] == value


def test_testrun_db_token(client):
    from testscheduler.models import TestRun
    from testscheduler.models import TestStatus

    json = {"username": "Francis", "env_id": 5, "path": "./"}
    ret = client.post("/api/testruns", json=json)
    assert ret.status_code == 201
    run_id = ret.get_json()["id"]

    obj = TestRun.query.get(run_id)
    assert hasattr(obj, "token")
    assert obj.status == getattr(TestStatus, "created")

    # Update the object and check if status was properly adjusted
    json = {"status": "failed", "token": obj.token}
    ret = client.post(f"/api/testruns/{run_id}", json=json)
    assert ret.status_code == 200
    assert ret.get_json()["status"] == "failed"
    assert obj.status == getattr(TestStatus, "failed")
