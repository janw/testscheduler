from flask import Flask
from flask_restful import Api
from flask_rq2 import RQ

application = Flask(
    __name__, static_url_path="/static", static_folder="../frontend/dist",
)
api = Api(application, prefix="/api")
rq = RQ(application)

from testexecutor import resources  # noqa: E402
from testexecutor import views  # noqa: E402, F401

api.add_resource(resources.TaskList, "/tasks")
api.add_resource(resources.Task, "/tasks/<task_id>")
