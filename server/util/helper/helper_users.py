"""users.py

Provides operational functions to the users blueprint.
"""

import psycopg2
from flask import g, request, session

from server.util import CitenoteError

from .helper_main import bcolors, citenote_check_hash, citenote_gen_hash, get_citenote_data


def validate_fields(field: str) -> str:
    """Validate the query provided by the user.

    Check weather query is provided by the user and returns the value of query.

    Variables:
        _val (any): stores the value from query

    Args:
        field (str): name of query string

    Returns:
        _val (str): value of query in string format

    Raises:
        ValueError: If the query is string is not present

    """

    _val = request.args.get(field)

    if not _val:
        raise ValueError

    return str(_val)


def get_role() -> str:
    """Provides the role for user.

    Get role from the users via query during login procedure. If the role is present in the allowed roles returns query
    value. If role is not present in the allowed roles returns "guest" as value.

    Variables:
        role (str): Role query provided by the user

    Returns:
        (str): value of role if present in allowed roles otherwise "guest"

    """

    role = request.args.get("role")

    if role in get_citenote_data("allowed_roles"):
        return role

    if role == "admin":
        raise CitenoteError.RoleError

    return "guest"


def users_login() -> bool:
    """Adds the user to the session.

    This function takes two mandatory query inputs from the user
        - username
        - password

    Function checks for provided username in database. If username found checks if stored password matches with provided
    password.

    Variables:
        username (str): username provided by user.
        password (str): password provided by user.
        errors (int): Tracks number of errors

    Returns:
        (bool): Returns true if no error occurs during the operation otherwise returns false.

    Raises:
        UsernameError: If username not found in database.
        PasswordError: If provided password does not match with password in database.

    """

    errors = 0

    try:
        username = validate_fields("username")
        password = validate_fields("password")

        get_user_query = get_citenote_data("get_user_query")
        get_password_hash_query = get_citenote_data("get_password_hash_query")

        cursor = g.db.cursor()
        cursor.execute(get_user_query, (username,))

        if not cursor.fetchone():
            raise CitenoteError.UsernameError

        cursor.execute(get_password_hash_query, (username,))
        pwhash = cursor.fetchone()[0]
        _check = citenote_check_hash(password, pwhash)

        if not _check:
            raise CitenoteError.PasswordError

        cursor.execute("select role from users where username= %s", (username,))
        role = cursor.fetchone()[0]
        cursor.close()
        return _check

    except CitenoteError.PasswordError as err:
        errors += 1
        bcolors.print_warning(err.message, err)

    except CitenoteError.UsernameError as err:
        errors += 1
        bcolors.print_warning(err.message, err)

    except (Exception, psycopg2.Error) as err:
        errors += 1
        print("Login failed ", err)

    finally:
        if errors:
            return False

        session.clear()
        session["username"] = username
        session["role"] = role


def users_register() -> bool:
    """Creates users in database.

    This function takes two mandatory query inputs and one optional input.
        - username
        - password
        - role (optional)

    Function stores id, username, encrypted password and role into the database.

    Variables:
        username (str): username provided by user.
        password (str): password provided by user.
        role (str): role provided by user.
        errors (int): Tracks number of errors


    Returns:
        (bool): Returns true if no error occurs during the operation otherwise returns false.

    Raises:
        UsernameError: If username not found in database.
        PasswordError: If provided password does not match with password in database.

    """

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


def users_delete() -> bool:
    """Delete user from the database.

    This function takes two mandatory query inputs from the user
        - username
        - password

    Function checks for provided username in database. If username found checks if stored password matches with provided
    password. If no error occurs the user is delete from the database.

    Variables:
        username (str): username provided by user.
        password (str): password provided by user.
        errors (int): Tracks number of errors

    Returns:
        (bool): Returns true if no error occurs during the operation otherwise returns false.

    Raises:
        UsernameError: If username not found in database.
        PasswordError: If provided password does not match with password in database.
    """

    errors = 0

    try:
        username = validate_fields("username")
        password = validate_fields("password")

        get_user_query = get_citenote_data("get_user_query")
        get_password_hash_query = get_citenote_data("get_password_hash_query")
        delete_user_query = get_citenote_data("delete_user_query")

        cursor = g.db.cursor()
        cursor.execute(get_user_query, (username,))

        if not cursor.fetchone():
            raise CitenoteError.UsernameError

        cursor.execute(get_password_hash_query, (username,))
        pwhash = cursor.fetchone()[0]
        _check = citenote_check_hash(password, pwhash)

        if not _check:
            raise CitenoteError.PasswordError

        cursor.execute(delete_user_query, (username,))
        g.db.commit()
        cursor.close()

    except CitenoteError.PasswordError as err:
        errors += 1
        bcolors.print_warning(err.message, err)

    except CitenoteError.UsernameError as err:
        errors += 1
        bcolors.print_warning(err.message, err)

    except (Exception, psycopg2.Error) as err:
        errors += 1
        print("Login failed ", err)

    finally:
        if errors:
            return False

    return True


def users_logout() -> bool:
    """Logouts user from the session

    Variables:
        errors (int): Count number of errors

    Returns:
        (bool): Returns true if no error occurs during the operation otherwise returns false.

    Raises:
        UsernameError: If username is not present in session
    """

    errors = 0

    try:
        if "username" not in session:
            raise CitenoteError.UsernameNotInSession

        session.clear()

    except CitenoteError.UsernameNotInSession as err:
        errors += 1
        bcolors.print_warning(err.message, err)

    except (Exception, psycopg2.Error) as err:
        errors += 1
        print("Logout failed ", err)

    finally:
        if errors:
            return False

        return True


if __name__ == "__main__":
    ...
