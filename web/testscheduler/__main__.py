import eventlet

eventlet.monkey_patch()

from testscheduler import create_app, socketio  # noqa: E402


def main():
    app = create_app()
    socketio.run(app)


main()
