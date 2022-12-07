from flask import Blueprint, g

from ..util.helper import connect_db
from ..util.helper.__users import users_login, users_register


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
def login():
    _check = users_login()

    if _check:
        return {"/": "login successful"}, 200
    return {"/": "login unsuccessful"}, 400


@_users.route("/register")
def register():
    _check = users_register()

    if _check:
        return {"/": "login successful"}, 200
    return {"/": "login unsuccessful"}, 400

    # try:
    #     _check = users_register()
    #     if not _check:
    #         raise ValueError

    #     return {"/": "registeration successful"}, 200

    # except ValueError:
    #     return {"/": "Bad request"}, 400

    # except Exception as err:
    #     print("Login failed due to: ", err)
    #     return {"/": "Internal server error"}, 500


@_users.route("/test")
def testing_func():
    return {}, 200
