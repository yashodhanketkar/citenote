from flask import Blueprint, request

from ..util.helper.helper_papers import (
    delete as delete_basic,
    get as get_basic,
    post as post_basic,
    update as update_basic,
)
from ..util.helper.helper_citations import (
    delete as delete_adv,
    get as get_adv,
    post as post_adv,
    update as update_adv,
)


_papers = Blueprint("papers", __name__, url_prefix="/papers")


@_papers.route("/about")
def about_papers():
    """Handles papers about route"""
    return {
        "message": "About papers",
    }, 200


@_papers.route("/", methods=("GET", "POST", "PATCH", "PUT", "DELETE"))
def papers_basic():
    """Handles papers basic routes"""
    match request.method:
        case "GET":
            return get_basic()
        case "POST":
            return post_basic()
        case "PATCH":
            return update_basic()
        case "PUT":
            return update_basic(replace=True)
        case "DELETE":
            return delete_basic()
        case _:
            return {"message": "_ method"}, 405


@_papers.route("/paper/<string:paper_id>", methods=("GET", "POST", "PATCH", "PUT", "DELETE"))
def papers_advance(paper_id):
    """Handles papers advance routes"""
    match request.method:
        case "GET":
            return get_adv(id=paper_id)
        case "POST":
            return post_adv(id=paper_id)
        case "PATCH":
            return update_adv(id=paper_id)
        case "PUT":
            return update_adv(id=paper_id, replace=True)
        case "DELETE":
            return delete_adv(id=paper_id)
        case _:
            return "<h1>_</h1>", 405
