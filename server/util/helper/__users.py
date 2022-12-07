import psycopg2
from flask import g, request
from .__main import citenote_check_hash, citenote_gen_hash, bcolors, get_citenote_data
from server.util import CitenoteError


def validate_fields(field: str) -> str:
    _val = request.args.get(field)
    if not _val:
        raise ValueError
    return _val


def get_role() -> str:

    role = request.args.get("role")
    if role in get_citenote_data("allowed_roles"):
        return role
    if role == "admin":
        raise CitenoteError.RoleError
    return "guest"


def users_login() -> bool:
    errors = 0
    try:
        username = validate_fields("username")
        password = validate_fields("password")

        get_user_query = get_citenote_data("get_user_query")
        get_password_hash_query = get_citenote_data("get_password_hash_query")

        cursor = g.db.cursor()
        cursor.execute(get_user_query)
        username_list = cursor.fetchall()[0]

        if username not in username_list:
            raise CitenoteError.UsernameError

        cursor.execute(get_password_hash_query, (username,))
        pwhash = cursor.fetchone()[0]
        _check = citenote_check_hash(password, pwhash)
        cursor.close()

        if not _check:
            raise CitenoteError.PasswordError

        return _check

    except CitenoteError.PasswordError as err:
        errors += 1
        bcolors.print_warning(err.message, err)

    except CitenoteError.UsernameError as err:
        errors += 1
        bcolors.print_warning(err.message, err)

    except (Exception, psycopg2.Error):
        errors += 1
        print("Login failed")

    finally:
        if errors:
            return False


def users_register() -> bool:
    errors = 0
    try:
        username = validate_fields("username")
        password = validate_fields("password")
        role = get_role()

        create_user_query = get_citenote_data("create_user_query")
        passwordhash = citenote_gen_hash(password)

        cursor = g.db.cursor()
        cursor.execute(create_user_query, (username, passwordhash, role))

        g.db.commit()
        cursor.close()

    except CitenoteError.RoleError as err:
        errors += 1
        bcolors.print_warning(err.message, err)

    except psycopg2.errors.UniqueViolation:
        errors += 1
        bcolors.print_warning("Username already exists", "UniqueViolation")

    except (Exception, psycopg2.Error) as err:
        errors += 1
        bcolors.print_warning(f"Registration failed {err}", "Unknown error")
    finally:
        if errors:
            return False
        return True


if __name__ == "__main__":
    ...
