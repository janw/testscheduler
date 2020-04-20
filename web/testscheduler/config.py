from os import environ
from os.path import dirname

from testrunner import TESTFILES_DIR  # noqa: F401

BASE_DIR = dirname(dirname(dirname(__file__)))

ENV = environ.get("FLASK_ENV", "production")
DEBUG = ENV == "development"
TESTING = ENV == "development"
SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False

RQ_REDIS_URL = environ.get("RQ_REDIS_URL", "redis://localhost:6379")
