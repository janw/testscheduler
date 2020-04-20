from contextlib import redirect_stderr
from contextlib import redirect_stdout
from io import StringIO
from os import environ
from os import chdir

import pytest
from requests import Session

from testrunner import TESTFILES_DIR
from testrunner import API_BASE

environ["COLUMNS"] = "120"

session = Session()


def post_status(id, token, **kwargs):
    session.post(API_BASE + f"/api/tasks/{id}", json={"token": token, **kwargs})


def run_test(id, path, token):
    post_status(id, token, status="running")
    chdir(TESTFILES_DIR)

    f = StringIO()
    with redirect_stdout(f):
        with redirect_stderr(f):
            return_val = pytest.main(["--color=yes", path])

    status = "succeeded" if return_val == 0 else "failed"
    logs = f.getvalue()
    post_status(id, token, status=status, logs=logs)
