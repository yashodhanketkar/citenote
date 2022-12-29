from flask import Blueprint, request

from ..util.helper.helper_papers import delete, get, post, update

_papers = Blueprint("papers", __name__, url_prefix="/papers")


@_papers.route("/about")
def about_papers():
    """Handles papers about route"""
    return {
        "message": "About papers",
    }, 200


@_papers.route("/", methods=("GET", "POST", "PATCH", "PUT", "DELETE"))
def papers_basic():
    """Handles papers basic route"""
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
            return {"message": "_ method"}, 405
