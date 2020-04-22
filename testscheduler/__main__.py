
import sys


def main(args):  # pragma: nocover
    if len(args) and args[0].lower() == "worker":
        from testscheduler.worker import run, register_signal_handlers

        register_signal_handlers()
        run()
    else:
        import eventlet

        eventlet.monkey_patch()

        from testscheduler.wsgi import app  # noqa: E401
        from testscheduler import socketio  # noqa: E401

        socketio.run(app)


main(sys.argv[1:])
