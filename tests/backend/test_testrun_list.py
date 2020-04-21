import pytest


def test_empty_testrun_list(client):
    """Tests the testruns list endpoint.

    List of test runs is expected to be empty here.
    """

    ret = client.get("/api/testruns")
    assert ret.status_code == 200
    assert ret.get_json() == []


def test_post_new_testrun(client):
    """Tests the testruns endpoint to create a new run.

    A new test run will be created and expected to match the output of the
    next GET to the same endpoint (as first list item).
    """

    json = {"username": "Peter", "env_id": 1, "path": "./tests/"}

    ret = client.post("/api/testruns", json=json)
    assert ret.status_code == 201
    json_post = ret.get_json()

    ret = client.get("/api/testruns")
    assert ret.status_code == 200
    assert len(ret.get_json()) == 1
    json_get = ret.get_json()

    for key, val in json.items():
        assert key in json_post
        assert key in json_get[0]
        assert json_post[key] == json_get[0][key] == val


@pytest.mark.parametrize(
    "json,expected_errors",
    [
        (None, ["_schema"]),
        ({"username": ""}, ["username", "env_id", "path"]),
        (
            {"username": 123, "env_id": 9999, "path": "/"},
            ["username", "env_id", "path"],
        ),
        ({"username": "Mary"}, ["env_id", "path"]),
        ({"path": "./"}, ["username", "env_id"]),
    ],
    ids=["no_data", "all_invalid_1", "all_invalid_2", "one_valid_1", "one_valid_2"],
)
def test_post_testrun_invalid(client, json, expected_errors):
    """Tests POSTing a test run with invalid data.

    Uses parametrized input that tries different combinations of invalid data,
    which are expected to show different entries for the `errors` list.
    """

    ret = client.post("/api/testruns", json=json)
    assert ret.status_code == 400
    resp = ret.get_json()
    assert "message" in resp
    assert "Data validation failed" in resp["message"]
    if expected_errors:
        assert "errors" in resp
        for err in expected_errors:
            assert err in resp["errors"]
