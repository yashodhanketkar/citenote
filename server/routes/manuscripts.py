from flask import Blueprint, request

from ..util.helper.helper_manuscripts import (
    add_paper,
    delete,
    get,
    get_paper,
    post,
    remove_paper,
    update,
)


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


@_manuscripts.route("/<string:manuscript_id>/add_paper/", methods=("GET", "POST", "PATCH", "DELETE"))
def manuscript_add_papers(manuscript_id):
    """Handles manuscript paper association routes"""
    match request.method:
        case "GET":
            return get_paper(manuscript_id=manuscript_id)
        case "POST" | "PATCH":
            return add_paper(manuscript_id=manuscript_id)
        case "DELETE":
            return remove_paper(manuscript_id=manuscript_id)
        case _:
            return {}, 500
