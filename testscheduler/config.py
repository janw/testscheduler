from os import environ
from os.path import dirname
from os.path import abspath
from os.path import join

BASE_DIR = dirname(dirname(abspath(__file__)))
DEFAULT_TESTFILES_DIR = join(BASE_DIR, "tests")

API_BASE = environ.get("SCHEDULER_API_BASE", "http://127.0.0.1:5000")

ENV = environ.get("FLASK_ENV", "production")
DEBUG = ENV == "development"
TESTING = ENV == "development" or environ.get("FLASK_TESTING", "").lower() == "true"

SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False

RQ_REDIS_URL = environ.get("RQ_REDIS_URL", "redis://localhost:6379")
TESTFILES_DIR = "tests"
PYTEST_BASE_ARGS = ["--color=yes", "-vv"]
