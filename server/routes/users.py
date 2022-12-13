from flask import Blueprint, g


from ..util.helper import connect_db
from ..util.helper.helper_users import users_delete, users_login, users_logout, users_register, users_operations


_users = Blueprint("users", __name__, url_prefix="/users")

connect_db(_users)


@_users.route("/users")
def get_user():
    cursor = g.db.cursor()
    add_user_query = """
    SELECT * FROM users
    """
    cursor.execute(add_user_query)
    users = cursor.fetchall()
    cursor.close()
    return {"/": "Get users", "users": users}, 200


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
