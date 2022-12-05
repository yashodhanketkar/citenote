from flask import Blueprint, request

_home = Blueprint("home", __name__, url_prefix="/home")


@_home.route("/", methods=("GET",))
def home():
    return {"home": "home page"}, 200


@_home.route("/about", methods=("GET",))
def about():
    return {"about": "This is home messgae"}, 200


@_home.route("/", methods=("GET",))
def get_id():
    _id = request.args.get("id")
    return {"function": "Returns user id", "id": _id}, 200
