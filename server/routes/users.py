from flask import Blueprint, request

from ..util.helper.helper_users import users_delete, users_login, users_logout, users_operations, users_register
from ..util.helper.helper_users import get_user_by_username, update_user_by_username


_users = Blueprint("users", __name__, url_prefix="/users")


@_users.route("/login")
@users_operations
def login():
    return users_login, "login"


@_users.route("/register")
@users_operations
def register():
    return users_register, "register"


@_users.route("/delete")
@users_operations
def delete_user():
    return users_delete, "delete user"


@_users.route("/logout")
@users_operations
def logout():
    return users_logout, "logout"


@_users.route("/<string:username>", methods=("GET", "PATCH"))
def users(username):
    match request.method:
        case "GET":
            get_user_by_username(username)

        case "PATCH":
            update_user_by_username(username)

        case _:
            return {}, 405

    return {}, 200
