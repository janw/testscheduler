from flask import Blueprint
from flask import current_app

base = Blueprint("base", __name__, url_prefix="/")


@base.route("/")
def index():
    return current_app.send_static_file("index.html")
