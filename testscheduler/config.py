from os import environ
from os.path import abspath
from os.path import dirname

BASE_DIR = dirname(dirname(abspath(__file__)))
TESTFILES_DIR = "tests"

API_BASE = environ.get("SCHEDULER_API_BASE", "http://127.0.0.1:5000")

ENV = environ.get("FLASK_ENV", "production")
DEBUG = ENV == "development"
TESTING = ENV == "development" or environ.get("FLASK_TESTING", "").lower() == "true"

SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False

REDIS_URL = environ.get("REDIS_URL", "redis://localhost:6379/1")
PYTEST_BASE_ARGS = ["--color=yes", "-vv", "--capture=no"]
PYTEST_EXTRA_ENV = {"COLUMNS": "120"}
