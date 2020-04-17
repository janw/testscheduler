from testexecutor import application


@application.route("/")
def index():
    return application.send_static_file("index.html")
