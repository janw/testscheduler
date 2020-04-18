import enum
from datetime import datetime

from testscheduler import db


class TestStatus(enum.Enum):
    created = 1
    running = 2
    succeeded = 3
    failed = 4
    unknown = 5


class TestRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    env_id = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(), nullable=False)
    status = db.Column(db.Enum(TestStatus), nullable=False, default=TestStatus.created)
    logs = db.Column(db.Text, nullable=False, default="")

    def __repr__(self):
        return f"<TestRun {self.id} (Env {self.env_id})>"


db.create_all()
