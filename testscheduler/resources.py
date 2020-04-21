from flask import request
from flask_restful import abort
from flask_restful import Resource
from marshmallow import ValidationError

from testscheduler import rq
from testscheduler import socketio
from testscheduler.models import db
from testscheduler.models import TestRun
from testscheduler.models import TestStatus
from testscheduler.schemas import testrun_logs
from testscheduler.schemas import testrun_logs_status
from testscheduler.schemas import testrun_schema
from testscheduler.schemas import testrun_schema_list
from testscheduler.worker import run_tests

job_queue = rq.get_queue()


def parse_args(loader):
    json_data = request.get_json()
    try:
        return loader.load(json_data)
    except ValidationError as err:
        abort(400, message="Data validation failed", errors=err.messages)


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
            abort(
                409, errors={"env_id": [f"Test environment {env_id} is already in use"]}
            )

        instance = TestRun(**data)
        db.session.add(instance)
        db.session.commit()

        job_queue.enqueue(
            run_tests, ttl=None, args=(instance.id, instance.path, instance.token)
        )
        dumped_instance = testrun_schema.dump(instance)
        socketio.emit("taskAdded", dumped_instance)
        return dumped_instance, 201


class TestRunDetail(Resource):
    def get(self, testrun_id):
        testrun = TestRun.query.get_or_404(testrun_id)
        return testrun_schema.dump(testrun)

    def post(self, testrun_id):
        data = parse_args(testrun_logs_status)
        instance = TestRun.query.get_or_404(testrun_id)
        if instance.token != data["token"]:
            abort(400, message="Invalid test run token")

        if "status" in data:
            instance.status = data["status"]
        if "logs" in data:
            instance.logs = data["logs"]
            socketio.emit("logsChanged", testrun_logs.dump(instance))

        db.session.commit()
        dumped_instance = testrun_schema.dump(instance)
        socketio.emit("taskChanged", dumped_instance)
        return dumped_instance


class TestRunLogs(Resource):
    def get(self, testrun_id):
        instance = TestRun.query.get_or_404(testrun_id)
        return testrun_logs.dump(instance)


class AvailableTestsList(Resource):
    def get(self):
        """Returns a list of available tests files for autocomplete."""
        from testscheduler.utils import testfiles

        return testfiles
