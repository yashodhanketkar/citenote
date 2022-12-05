from flask import Blueprint, g
from ..util.database import connect_db, init_db
from ..util.helper import citenote_check_hash, citenote_gen_hash, create_admin

# from werkzeug.security import check_password_hash, generate_password_hash

_users = Blueprint("users", __name__, url_prefix="/users")

connect_db(_users)


@_users.route("/admin")
def admin():
    init_db()
    create_admin()
    return {"/": "Created admin"}, 200


@_users.route("/add")
def add_user():
    # cursor = g.db.cursor()
    # cursor.close()
    pass_1 = "hello"
    hash_1, salt = citenote_gen_hash(pass_1)
    check = citenote_check_hash(pass_1, salt, hash_1)
    print("Check: ", check)

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
