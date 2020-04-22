import logging
import json
import signal
import subprocess
import sys
from collections import deque
from os import environ
from threading import Event
from threading import Thread
from time import sleep

import logzero
from requests_futures.sessions import FuturesSession
from typing import Dict

from testscheduler import create_app

LOG_FORMAT = (
    "%(color)s[%(levelname)1.1s %(asctime)s %(threadName)s]%(end_color)s %(message)s"
)
LOG_LEVEL = logging.INFO

formatter = logzero.LogFormatter(fmt=LOG_FORMAT)
logger = logzero.setup_default_logger(formatter=formatter, level=LOG_LEVEL)
session = FuturesSession()


# Common thread reference structure, for accessing statuses.
thread_refs: Dict[int, Thread] = {}


class BaseThread(Thread):
    name_suffix = "Base"

    def __init__(self, **kwargs):
        super().__init__()
        self.env_id = kwargs.pop("env_id")
        self.name = f"EnvThread{self.name_suffix}-{self.env_id:03d}"
        self.daemon = True

        # Assign rest of kwargs to class properties
        for key, val in kwargs.items():
            setattr(self, key, val)

    def post_status(self, _tries=3, _retry_delay=1, **kwargs):
        """Posts the status to the API for a given test run ID.

        By default an unsuccessful attempt will be retried twice (3 tries total)
        until a error raises an exception.
        """
        api_base, id, token = self.status_args
        url = api_base + f"/api/testruns/{id}"
        payload = {"token": token, **kwargs}
        while _tries > 0:
            resp = session.post(url, json=payload)
            resp = resp.result()
            if resp.status_code < 400:
                break
            _tries -= 1
            logger.error(
                f"Failed updating test run {id}, trying {_tries} more time(s)."
            )
            sleep(_retry_delay)


class LogConsumerThread(BaseThread):
    """Thread to consume the logs from the pytest subprocess and forward them.

    The consumer attaches to the provided `pipe` fileobject and consumes it
    line-wise, forwarding the contents to the provided `consumer`. After the
    object is exhausted (signalled by an empty string). the fileobject is
    closed.
    """

    name_suffix = "LogConsumer"

    def run(self):
        logger.info("Attaching to pipe")
        for line in iter(self.pipe.readline, ""):
            self.consumer(line)
        logger.info("Pipe exhausted. Closing.")
        self.pipe.close()


class LogPublisherThread(BaseThread):
    """Thread to ship updated logs to the API during the test run.

    The thread accesses the open file object which pytest logs are written to
    and thus provides "provisional" results to the backend for storage.
    """

    name_suffix = "LogPusher"
    check_interval = 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stop_event = Event()

    def run(self):
        prev_state = ""
        while True:
            sleep(self.check_interval)
            current_logs = "".join(self.out)
            if current_logs != prev_state:
                logger.debug("Updating logs")
                self.post_status(logs=current_logs)
                prev_state = current_logs
            if self.stop_event.wait(0):
                break


class RunnerThread(BaseThread):
    """Runs the tests and handles all logic related to it.

    The runner spawns two additional threads for processing and publishing the
    log output of the test run. This specifically allows for intermediate
    period updates of the log output towards the API.
    """

    name_suffix = "Runner"

    def run(self):
        logger.info(f"Hello from {self.name}")
        self.post_status(status="running")

        cmd = self.proc_args.pop("cmd")
        process = subprocess.Popen(
            cmd,
            **self.proc_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            close_fds=True,
            bufsize=1,
            universal_newlines=True,
        )

        # Start helper threads (log consumer and publisher) using common deque
        self.out = deque()
        logcon = LogConsumerThread(
            env_id=self.env_id, pipe=process.stdout, consumer=self.out.append
        )
        logpub = LogPublisherThread(
            env_id=self.env_id, status_args=self.status_args, out=self.out
        )
        logcon.start()
        logpub.start()

        logger.info("Running. Waiting for test run to finish")
        process.wait()

        logger.info("Tests finished. Tearing down.")
        logpub.stop_event.set()
        logpub.join()
        logcon.join()

        status = "succeeded" if process.returncode == 0 else "failed"
        self.post_status(status=status, logs="".join(self.out))
        logger.info("Published final status/logs. Bye.")


def run():
    """Runs the background worker continuously for processing test runs.

    The worker will connect to Redis and wait for new jobs coming in. The job
    payload will be transformed into the required processing arguments. A
    RunnerThread instance will be spawned with those arguments, and handles all
    the actual test execution logic.
    """

    app = create_app()
    api_base = app.config["API_BASE"]
    pytest_args = app.config["PYTEST_BASE_ARGS"]
    base_dir = app.config["BASE_DIR"]

    pytest_env = environ.copy()
    pytest_env.update(app.config["PYTEST_EXTRA_ENV"])

    logger.info(f"Will talk to API at {api_base}")
    logger.info(f"Entering standby for receiving tasks")
    while True:
        alive_count = len([env_id for env_id, t in thread_refs.items() if t.is_alive()])
        logger.debug(f"Standing by for new tasks ({alive_count} running)")
        testrun = app.redis.blpop("testruns", timeout=60)
        if not testrun:
            continue
        payload = json.loads(testrun[1])
        env_id = payload["env_id"]
        if env_id in thread_refs and thread_refs[env_id].is_alive():
            logger.error(
                f"Cannot execute: env {env_id} is already in use. Dropping task."
            )
            continue
        proc_args = {
            "cmd": ["python", "-m", "pytest", *pytest_args, payload["path"]],
            "env": pytest_env,
            "cwd": base_dir,
        }
        status_args = [api_base, payload["id"], payload["token"]]
        task = RunnerThread(
            env_id=env_id, proc_args=proc_args, status_args=status_args,
        )
        task.start()
        thread_refs[env_id] = task


def register_signal_handlers():
    """Registers signal handlers for gracefully shutting down the worker.

    This allows for running tasks to properly finish before the program exists.
    """

    def handle_signal(sig, frame):
        logger.info(f"Received signal {signal.Signals(sig).name}")

        for env_id, task in thread_refs.items():
            logger.info(f"Joining worker for env {env_id}")
            task.join()

        logger.info("All done. Bye.")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
