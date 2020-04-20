import os
import tempfile

import pytest

from testscheduler import create_app

app = create_app()


@pytest.fixture(scope="module")
def client():
    db_fd, tempdb = tempfile.mkstemp()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + tempdb

    ctx = app.app_context()
    ctx.push()
    from testscheduler.models import db

    db.create_all()

    with app.test_client() as client:
        yield client

    ctx.pop()
    os.close(db_fd)
    os.unlink(tempdb)


@pytest.fixture(scope="module")
def dbraw(client):

    with client.application.app_context():
        from testscheduler.models import db

        yield db
