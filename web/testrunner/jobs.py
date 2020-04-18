from io import StringIO
from os import environ
from contextlib import redirect_stdout
from contextlib import redirect_stderr

import pytest
from requests import Session


API_BASE = "http://127.0.0.1:5000"
environ["COLUMNS"] = "120"

session = Session()


def run_test(id, path, token):
    f = StringIO()
    with redirect_stdout(f):
        with redirect_stderr(f):
            return_val = pytest.main(["--color=yes", path])

    status = "succeeded" if return_val == 0 else "failed"
    logs = f.getvalue()

    resp = session.post(
        API_BASE + f"/api/tasks/{id}",
        json={"token": token, "status": status, "logs": logs},
    )
    resp.raise_for_status()
    return logs
