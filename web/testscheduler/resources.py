from flask_restful import Resource
from flask_restful import marshal_with
from werkzeug import exceptions

from testrunner.jobs import run_test

from testscheduler import db
from testscheduler import rq
from testscheduler.models import TestRun
from testscheduler.models import TestStatus
from testscheduler.marshalling import testrun_fields
from testscheduler.formatting import format_logs
from testscheduler.parsers import create_parser, update_parser

queue = rq.get_queue()


class TaskList(Resource):
    @marshal_with(testrun_fields)
    def get(self):
        runs = TestRun.query.all()
        return runs

    @marshal_with(testrun_fields)
    def post(self):
        args = create_parser.parse_args()
        env_id = args["env_id"]
        if TestRun.query.filter(
            (TestRun.env_id == env_id)
            & (
                (TestRun.status == TestStatus.created)
                | (TestRun.status == TestStatus.running)
            )
        ).count():
            raise exceptions.Conflict(f"Test env {env_id} is already in use")

        # TODO: validate `path`

        t = TestRun(**args)
        db.session.add(t)
        db.session.commit()

        queue.enqueue(run_test, args=(t.id, t.path, "tokendummy"))
        return t, 201


class Task(Resource):
    @marshal_with(testrun_fields)
    def get(self, task_id):
        return TestRun.query.get_or_404(task_id)

    @marshal_with(testrun_fields)
    def post(self, task_id):
        args = update_parser.parse_args()
        instance = TestRun.query.get_or_404(task_id)
        instance.status = getattr(TestStatus, args["status"])
        if args["logs"]:
            instance.logs = args["logs"]

        db.session.commit()

        return instance


class TaskLogs(Resource):
    def get(self, task_id):
        instance = TestRun.query.get_or_404(task_id)
        if instance.logs:
            return format_logs(instance.logs)

        return None


class TestList(Resource):
    def get(self):
        # Return list of available/runnable tests for autocomplete
        pass
