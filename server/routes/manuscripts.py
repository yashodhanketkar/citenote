from flask import Blueprint, request

from ..util.helper.helper_manuscripts import get, post, update, delete


_manuscripts = Blueprint("manuscripts", __name__, url_prefix="/manuscripts")


@_manuscripts.route("/about", methods=("GET", "POST"))
def manuscripts_about():
    return {
        "/": "About page of manuscripts",
    }


@_manuscripts.route("/", methods=("GET", "POST", "PATCH", "PUT", "DELETE"))
def manuscript_basic():
    match request.method:
        case "GET":
            return get()
        case "POST":
            return post()
        case "PATCH":
            return update()
        case "PUT":
            return update()
        case "DELETE":
            return delete()
        case _:
            return {}, 500
