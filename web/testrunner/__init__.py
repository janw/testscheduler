from os import environ
from os.path import dirname, abspath, join

DEFAULT_TESTFILES_DIR = join(dirname(dirname(dirname(abspath(__file__)))), "tests")
TESTFILES_DIR = environ.get("RUNNER_TESTFILES_DIR", DEFAULT_TESTFILES_DIR)
