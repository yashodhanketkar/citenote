from flask import Blueprint

from ..models.users import User, db
from ..util.helper.helper_users import (users_delete, users_login,
                                        users_logout, users_operations,
                                        users_register)

_users = Blueprint("users", __name__, url_prefix="/users")

# connect_db(_users)


@_users.route("/get/<string:username>")
def get_user(username):
    print(username)
    user = db.one_or_404(db.select(User).filter_by(username=username), description=f"No user named '{username}'.")
    return {"/": "Get users", "users": user.username}, 200


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


@_users.route("/test")
def testing_func():
    return {}, 200
