from flask import Flask
from flask_restful import Api
from flask_rq2 import RQ
from flask_socketio import SocketIO

socketio = SocketIO(path="/sock", async_mode="eventlet", cookie=None)
api = Api(prefix="/api", catch_all_404s=True)
rq = RQ()


def create_app(debug=False):
    app = Flask(__name__, static_url_path="/static", static_folder="../frontend/dist",)
    app.config.from_object("testscheduler.config")

    socketio.init_app(app)
    rq.init_app(app)

    # Set up database and ensure tables are created
    from testscheduler.models import db

    db.init_app(app)
    db.create_all(app=app)

    # Register API endpoints
    from testscheduler import resources  # noqa: E402

    api.add_resource(resources.TestRunList, "/testruns")
    api.add_resource(resources.TestRunDetail, "/testruns/<testrun_id>")
    api.add_resource(resources.TestRunLogs, "/testruns/<testrun_id>/logs")
    api.add_resource(resources.AvailableTestsList, "/tests")
    api.init_app(app)

    # Add base blueprint that serves the static index.html at '/'
    from testscheduler.views import base

    app.register_blueprint(base)

    return app
