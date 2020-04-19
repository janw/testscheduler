from testscheduler import application as app


@app.route("/")
def index():
    return app.send_static_file("index.html")
