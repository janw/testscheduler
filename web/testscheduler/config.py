from os import environ
from os.path import dirname, join

BASE_DIR = dirname(dirname(dirname(__file__)))

ENV = environ.get("FLASK_ENV", "production")
DEBUG = ENV == "development"
TESTING = ENV == "development"
SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False
TESTFILES_DIR = join(BASE_DIR, "tests")
