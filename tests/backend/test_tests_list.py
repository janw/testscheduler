from os.path import exists


def test_tests_list(client):
    """Tests the tests list endpoint.

    List of tests is expected contain all files from /tests
    """

    ret = client.get("/api/tests")
    assert ret.status_code == 200
    tests = ret.get_json()

    for entry in tests:
        assert entry.startswith("./tests")
        assert "conftest" not in entry
        assert exists(entry)

    for expected in ("./tests/backend/", "./tests/backend/test_tests_list.py"):
        assert expected in tests
