from flask import Blueprint, request

from ..util.helper.helper_manuscripts import delete, get, post, update


_manuscripts = Blueprint("manuscripts", __name__, url_prefix="/manuscripts")


@_manuscripts.route("/about", methods=("GET", "POST"))
def manuscripts_about():
    """Handles manuscripts about route"""
    return {
        "/": "About page of manuscripts",
    }, 200


@_manuscripts.route("/", methods=("GET", "POST", "PATCH", "PUT", "DELETE"))
def manuscript_basic():
    """Handles manuscripts basic route"""
    match request.method:
        case "GET":
            return get()
        case "POST":
            return post()
        case "PATCH":
            return update()
        case "PUT":
            return update(replace=True)
        case "DELETE":
            return delete()
        case _:
            return {}, 500
