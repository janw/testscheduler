DUMMY_LOGS = "Lorem ipsum dolor sit amet"


def test_testrun_logs(client):
    """Tests the testruns logs endpoint.

    A new test run will be created and the logs bool is expected to match
    the existence of log data. Accessing the …/logs endpoint should return
    an HTML structure of a Pygments .highlighttable, which contains the logs
    embedded and properly rendered.
    """
    from testscheduler.models import TestRun

    json = {"username": "John", "env_id": 1, "path": "./tests/"}
    ret = client.post("/api/testruns", json=json)
    assert ret.status_code == 201
    json_post = ret.get_json()

    entry_id = json_post["id"]
    ret = client.get(f"/api/testruns/{entry_id}")
    assert ret.status_code == 200
    data = ret.get_json()
    assert data["logs"] is False

    # Retrieve token to be able to POST an update
    token = TestRun.query.get(data["id"]).token
    json_post = {"token": token, "logs": DUMMY_LOGS}

    ret = client.post(f"/api/testruns/{entry_id}", json=json_post)
    assert ret.status_code == 200

    # Get the entry again, logs should be True now
    ret = client.get(f"/api/testruns/{entry_id}")
    assert ret.status_code == 200
    data = ret.get_json()
    assert data["logs"] is True

    # Get actual logs and verify HTML format
    ret = client.get(f"/api/testruns/{entry_id}/logs")
    assert ret.status_code == 200
    logs = ret.get_json()["logs"]
    assert logs.startswith('<table class="highlighttable">')
    assert logs.endswith("</table>")
    assert DUMMY_LOGS in logs
