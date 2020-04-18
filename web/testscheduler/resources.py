from flask_restful import Resource
from flask_restful import reqparse, inputs, marshal_with

from testscheduler import db
from testscheduler.models import TestRun
from testscheduler.models import TestStatus
from testscheduler.marshalling import testrun_fields
from testscheduler.marshalling import testrun_fields_with_logs

ENV_ID_RANGE = (1, 100)

parser = reqparse.RequestParser()
parser.add_argument(
    "username", required=True, type=str, help="Invalid Username for the test to be run"
)
parser.add_argument(
    "env_id", required=True, type=inputs.int_range(*ENV_ID_RANGE), help="{error_msg}",
)
parser.add_argument("path", required=True, help="Invalid path of tests to be run")


class TaskList(Resource):
    @marshal_with(testrun_fields)
    def get(self):
        runs = TestRun.query.all()
        return runs

    @marshal_with(testrun_fields)
    def post(self):
        args = parser.parse_args()
        env_id = args["env_id"]
        if TestRun.query.filter(
            (TestRun.env_id == env_id)
            & (
                (TestRun.status == TestStatus.created)
                | (TestRun.status == TestStatus.running)
            )
        ).count():
            raise reqparse.exceptions.Conflict(f"Test env {env_id} is already in use")

        # TODO: validate `path`

        t = TestRun(**args)
        db.session.add(t)
        db.session.commit()

        return t, 201


class Task(Resource):
    @marshal_with(testrun_fields_with_logs)
    def get(self, task_id):
        return TestRun.query.get_or_404(task_id)


class TestList(Resource):
    def get(self):
        # Return list of available/runnable tests for autocomplete
        pass
