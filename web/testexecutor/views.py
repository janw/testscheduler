from testexecutor import application


@application.route("/")
def index():
    # Serve SPA here
    return ""
