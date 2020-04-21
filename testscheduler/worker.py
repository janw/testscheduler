import traceback
from contextlib import redirect_stderr
from contextlib import redirect_stdout
from io import StringIO
from os import chdir
from os import environ
from threading import Event
from threading import Thread
from time import sleep

import pytest
from requests import Session

from testscheduler import create_app

environ["COLUMNS"] = "120"
session = Session()
stop_event = Event()


def post_status(api_base, id, token, _tries=3, _retry_delay=5, **kwargs):
    """Posts the status to the API for a given test run ID.

    By default an unsuccessful attempt will be retried twice (3 tries total)
    until a error raises an exception.
    """
    url = api_base + f"/api/testruns/{id}"
    payload = {"token": token, **kwargs}
    while _tries > 0:
        resp = session.post(url, json=payload)
        if resp.status_code < 400:
            break
        _tries -= 1
        sleep(_retry_delay)
    resp.raise_for_status()


class UpdateLogs(Thread):
    """Thread to ship updated logs to the API during the test run.

    The thread accesses the open file object which pytest logs are written to
    and thus provides "provisional" results to the backend for storage.
    """

    def __init__(self, f, api_base, id, token, interval=3):
        super().__init__()
        self.f = f
        self.api_base = api_base
        self.job_id = id
        self.job_token = token
        self.check_interval = interval

    def run(self):
        prev_state = ""
        while True:
            sleep(self.check_interval)
            current_logs = self.f.getvalue()
            if current_logs != prev_state:
                post_status(
                    self.api_base, self.job_id, self.job_token, logs=current_logs
                )
                prev_state = current_logs
            if stop_event.wait(0):
                break


def run_tests(id, path, token):
    """Runs the given path of tests through pytest.

    During the test run, a `UpdateLogs` background thread is periodically
    updating the logs status with the backend.
    """
    app = create_app()
    api_base = app.config["API_BASE"]
    base_dir = app.config["BASE_DIR"]
    base_args = app.config["PYTEST_BASE_ARGS"]
    post_status(api_base, id, token, status="running")
    f = StringIO()
    t = UpdateLogs(f, api_base, id, token)
    t.start()
    with redirect_stdout(f):
        with redirect_stderr(f):
            try:
                # Create app instance for access to .config
                chdir(base_dir)
                return_val = pytest.main([*base_args, path])
            except Exception:
                f.write(traceback.format_exc())
                return_val = -1
    stop_event.set()
    t.join()
    logs = f.getvalue()
    status = "succeeded" if return_val == 0 else "failed"
    post_status(api_base, id, token, status=status, logs=logs)
