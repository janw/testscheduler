from flask import Flask
from flask_restful import Api
from flask_rq2 import RQ
from flask_sqlalchemy import SQLAlchemy

application = Flask(
    __name__, static_url_path="/static", static_folder="../frontend/dist",
)
application.config.from_object("testscheduler.config")

api = Api(application, prefix="/api")
db = SQLAlchemy(application)
rq = RQ(application)

from testscheduler import models  # noqa: E402, F401
from testscheduler import resources  # noqa: E402
from testscheduler import views  # noqa: E402, F401

api.add_resource(resources.TaskList, "/tasks")
api.add_resource(resources.Task, "/tasks/<task_id>")
api.add_resource(resources.TaskLogs, "/tasks/<task_id>/logs")
api.add_resource(resources.TestList, "/tests")
