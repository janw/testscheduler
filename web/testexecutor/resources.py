from flask_restful import Resource
from flask_restful import abort, reqparse, inputs

TASKS = {}  # Database dummy
ENV_ID_RANGE = (1, 100)

parser = reqparse.RequestParser()
parser.add_argument(
    "username", required=True, type=str, help="User requesting the test to be run"
)
parser.add_argument(
    "env_id",
    required=True,
    type=inputs.int_range(*ENV_ID_RANGE),
    help="ID for the environment to run the test in",
)
parser.add_argument(
    "tests", required=True, help="Comma-separated list of tests to be run"
)


class TaskList(Resource):
    def get(self):
        return TASKS

    def post(self):
        args = parser.parse_args()
        if len(TASKS) == 0:
            task_id = 1
        else:
            task_id = max(TASKS.keys()) + 1

        args["tests"] = args["tests"].split(",")
        TASKS[task_id] = args
        return TASKS[task_id], 201


class Task(Resource):
    def get(self, task_id):
        if task_id not in TASKS:
            abort(404, message=f"Task {task_id} doesn't exist")
        return TASKS[task_id]


class TestList(Resource):
    def get(self):
        # Return list of available/runnable tests for autocomplete
        pass
