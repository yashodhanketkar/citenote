from flask import Blueprint, g

from ..util.helper import connect_db


_users = Blueprint("users", __name__, url_prefix="/users")

connect_db(_users)


@_users.route("/add")
def add_user():
    return {"/": "Add users"}, 200


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
