import eventlet

eventlet.monkey_patch()

from testscheduler.wsgi import app  # noqa: E401
from testscheduler import socketio  # noqa: E401

socketio.run(app)
