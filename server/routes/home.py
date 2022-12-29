from flask import Blueprint

from ..util.helper.helper_main import get_config, get_version


_home = Blueprint("home", __name__)


@_home.route("/", methods=("GET",))
def home_home():
    """Handles get home route"""
    return {"message": "This is home page"}, 200


@_home.route("/about", methods=("GET",))
def home_about():
    """Handles about home route"""
    return {
        "name": get_config("name"),
        "version": get_version(),
        "description": get_config("description"),
        "author": get_config("author"),
        "contact": get_config("author_email"),
    }, 200
