import secrets
from flask import g
from werkzeug.security import check_password_hash, generate_password_hash

method = "pbkdf2:sha256"


def citenote_gen_hash(password: str) -> (str, str):
    salt = secrets.token_hex(20)
    salted_pass = f"{method}${password}${salt}"
    return generate_password_hash(salted_pass), salt


def citenote_check_hash(password, salt, hash):
    salted_pass = f"{method}${password}${salt}"
    return check_password_hash(hash, salted_pass)


def create_admin():
    create_admin_query = """
    insert into users (id, username, password, salt, role)
    Values (%s, %s, %s, %s, %s);
    """
    password, salt = citenote_gen_hash("admin")
    admin_default = (9999, "admin", password, salt, "admin")
    cursor = g.db.cursor()
    cursor.execute(create_admin_query, admin_default)
    g.db.commit()
    cursor.close()
