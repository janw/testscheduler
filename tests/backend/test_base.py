def test_serving_spa(client):
    """Tests serving the SPA from '/'"""

    ret = client.get("/")
    assert ret.status_code == 200
    assert b'script inline src="/static/' in ret.data
