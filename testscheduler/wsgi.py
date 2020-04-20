from testscheduler import create_app

app = create_app()

from testscheduler.models import db  # noqa: E402

db.create_all(app=app)
