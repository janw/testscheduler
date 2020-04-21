from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO
from redis import Redis

socketio = SocketIO(path="/sock", async_mode="eventlet", cookie=None)


def create_app(debug=False):
    app = Flask(__name__, static_url_path="/static", static_folder="../frontend/dist")
    app.config.from_object("testscheduler.config")

    # Socket.IO for handling frontend interactivity
    socketio.init_app(app)

    # Redis for worker communication
    app.redis = Redis.from_url(app.config["REDIS_URL"])

    # Set up database and ensure tables are created
    from testscheduler.models import db

    db.init_app(app)

    # Register API endpoints
    from testscheduler import resources  # noqa: E402

    api = Api(prefix="/api", catch_all_404s=True)
    api.add_resource(resources.TestRunList, "/testruns")
    api.add_resource(resources.TestRunDetail, "/testruns/<testrun_id>")
    api.add_resource(resources.TestRunLogs, "/testruns/<testrun_id>/logs")
    api.add_resource(resources.AvailableTestsList, "/tests")
    api.init_app(app)

    # Add base blueprint that serves the static index.html at '/'
    from testscheduler.views import base

    app.register_blueprint(base)

    return app
