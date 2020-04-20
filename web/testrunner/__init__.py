from os import environ
from os.path import dirname, abspath, join

DEFAULT_TESTFILES_DIR = join(dirname(dirname(abspath(__file__))), "tests")
TESTFILES_DIR = environ.get("RUNNER_TESTFILES_DIR", DEFAULT_TESTFILES_DIR)
API_BASE = environ.get("SCHEDULER_API_BASE", "http://127.0.0.1:5000")
