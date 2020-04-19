from flask import request
from flask_restful import abort
from flask_restful import Resource
from marshmallow import ValidationError

from testrunner.jobs import run_test
from testscheduler import db
from testscheduler import rq
from testscheduler.schemas import testrun_schema
from testscheduler.schemas import testrun_schema_list
from testscheduler.schemas import testrun_logs
from testscheduler.schemas import testrun_logs_status
from testscheduler.models import TestRun
from testscheduler.models import TestStatus
from testscheduler.utils import testfiles

queue = rq.get_queue()


def parse_args(loader):
    json_data = request.get_json()
    if not json_data:
        abort(400, message="No input data provided")
    try:
        return loader.load(json_data)
    except ValidationError as err:
        abort(422, message="Data validation failed", errors=err.messages)


class TestRunList(Resource):
    def get(self):
        runs = TestRun.query.order_by(TestRun.id.desc()).all()
        return testrun_schema_list.dump(runs)

    def post(self):
        data = parse_args(testrun_schema)
        env_id = data["env_id"]

        if TestRun.query.filter(
            (TestRun.env_id == env_id)
            & (
                (TestRun.status == TestStatus.created)
                | (TestRun.status == TestStatus.running)
            )
        ).count():
            abort(409, env_id=[f"Test environment {env_id} is already in use"])

        instance = TestRun(**data)
        db.session.add(instance)
        db.session.commit()

        job = queue.enqueue(run_test, args=(instance.id, instance.path, "tokendummy"))
        print(job)
        return testrun_schema.dump(instance), 201


class TestRunDetail(Resource):
    def get(self, task_id):
        testrun = TestRun.query.get_or_404(task_id)
        return testrun_schema.dump(testrun)

    def post(self, task_id):
        data = parse_args(testrun_logs_status)
        instance = TestRun.query.get_or_404(task_id)
        if "status" in data:
            instance.status = data["status"]
        if "logs" in data:
            instance.logs = data["logs"]

        db.session.commit()
        return testrun_schema.dump(instance)


class TestRunLogs(Resource):
    def get(self, task_id):
        instance = TestRun.query.get_or_404(task_id)
        return testrun_logs.dump(instance)


class AvailableTestsList(Resource):
    def get(self):
        """Returns a list of available tests files for autocomplete."""
        return testfiles
