from flask import Blueprint, request


_papers = Blueprint("papers", __name__, url_prefix="/papers")


@_papers.route("/about")
def about_papers():
    return {
        "message": "About papers",
    }, 200


@_papers.route("/", methods=("GET", "POST", "PATCH", "PUT", "DELETE"))
def papers_basic():
    match request.method:
        case "GET":
            return {"message": "Get method"}, 200
        case "POST":
            return {"message": "Post method"}, 200
        case _:
            return {"message": "_ method"}, 405
