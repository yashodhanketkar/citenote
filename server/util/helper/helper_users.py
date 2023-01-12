"""users.py

Provides operational functions to the users blueprint.
"""

import functools
from datetime import datetime
from typing import Callable, Literal, Tuple

import psycopg2
import psycopg2.errors as pgerr
from flask import request, session

from ...models.users import User, db
from ..CitenoteError import (
    PasswordError,
    RoleError,
    UsernameError,
    UsernameInSession,
    UsernameNotInSession,
)
from .helper_main import (
    bcolors,
    citenote_check_hash,
    citenote_gen_hash,
    get_citenote_data,
    get_form_data,
)


def validate_fields(field: str) -> str:
    """Validate the query provided by the user.

    Check weather query is provided by the user and returns the value of query.

    Args:
        field (str): name of query string

    Variables:
        _val (any): stores the value from query

    Returns:
        _val (str): value of query in string format

    Raises:
        ValueError: If the query is string is not present

    """

    _val = request.args.get(field)

    if not _val:
        raise ValueError

    return str(_val)


def role_validator(role: str | None) -> str:
    """Validates provided role

    Args:
        role (str): Provided role

    Returns:
        role (str): Role if it's valid or guest.

    Raises:
        RoleError: Raise if "admin" role is requested.
    """
    if role:
        if role == "admin":
            raise RoleError

        if role in get_citenote_data("allowed_roles"):
            return role

    return "guest"


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
    return role_validator(role)


def users_operations(ufunc: Callable) -> Callable:
    """User operations handler for user routes

    This function provided output view to the user routes.

    Args:
        ufunct (Callable): Route functions name

    Variables:
        _check (Callable -> bool): Function assigend to the route, returns boolean value
        name (str): Name of operation

    Returns:
        wrapper (tuple): Returns output (dict -> json) and status code

    """

    @functools.wraps(ufunc)
    def wrapper() -> Tuple[dict, int]:
        _check, name = ufunc()
        if _check():
            return {"check": f"{name} successful"}, 200
        return {"check": f"{name} unsuccessful"}, 400

    return wrapper


def users_login() -> bool:
    """Adds the user to the session.

    This function takes two mandatory query inputs from the user
        - username
        - password

    Function checks for provided username in database. If username found checks if stored password matches with provided
    password.

    Variables:
        errors (int): Tracks number of errors
        request_time (datetime): Time of request at server.
        username (str): username provided by user.
        password (str): password provided by user.
        user (User): User class

    Returns:
        (bool): Returns true if no error occurs during the operation otherwise returns false.

    Raises:
        UsernameInSession: If user is already logged in.
        UsernameError: If username not found in database.
        PasswordError: If provided password does not match with password in database.

    """

    errors = 0
    request_time = datetime.now()

    try:
        if "username" in session:
            raise UsernameInSession

        username = validate_fields("username")
        password = validate_fields("password")

        user: User = User.query.filter_by(username=username).first()
        if not user:
            raise UsernameError

        if not citenote_check_hash(password, user.password):
            raise PasswordError

        user.last_login = request_time
        db.session.commit()

        session["username"] = user.username
        session["role"] = user.role
        print(f"{username = } logged in session\n{request_time}")

    except (UsernameInSession, UsernameError, PasswordError) as err:
        errors += 1
        err.print_error()

    except (Exception, psycopg2.Error) as err:
        errors += 1
        bcolors.print_warning("Login failed", repr(err))

    finally:
        if errors:
            return False

        return True


def users_register() -> bool:
    """Creates users in database.

    This function takes two mandatory query inputs and one optional input.
        - username
        - password
        - role (optional)

    Function stores id, username, encrypted password and role into the database.

    Variables:
        errors (int): Tracks number of errors
        request_time (datetime): Time of request at server.
        username (str): username provided by user.
        password (str): password provided by user.
        role (str): role provided by user.
        user (User): User class

    Returns:
        (bool): Returns true if no error occurs during the operation otherwise returns false.

    Raises:
        UsernameError: If username not found in database.
        PasswordError: If provided password does not match with password in database.

    """

    errors = 0
    request_time = datetime.now()

    try:
        username = validate_fields("username")
        password = validate_fields("password")
        role = get_role()

        if User.query.filter_by(username=username).first():
            raise pgerr.UniqueViolation

        user = User(username, citenote_gen_hash(password), role)
        user.date_joined = request_time
        db.session.add(user)
        db.session.commit()

        print(f"{username = } registered in database")

    except RoleError as err:
        errors += 1
        err.print_error()

    except pgerr.UniqueViolation as err:
        errors += 1
        bcolors.print_warning("Username already exists", repr(err))

    except (Exception, psycopg2.Error) as err:
        errors += 1
        bcolors.print_warning("Registration failed", repr(err))

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
        errors (int): Tracks number of errors
        username (str): username provided by user.
        password (str): password provided by user.
        user (User): User class

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

        user = User.query.filter_by(username=username).first()

        if not user:
            raise UsernameError

        if not citenote_check_hash(password, user.password):
            raise PasswordError

        db.session.delete(user)
        db.session.commit()

        print(f"{username = } deleted from database")

    except (PasswordError, UsernameError) as err:
        errors += 1
        err.print_error()

    except (Exception, psycopg2.Error) as err:
        errors += 1
        bcolors.print_warning("Removal failed", repr(err))

    finally:
        if errors:
            return False

        session.clear()
        return True


def users_logout() -> bool:
    """Logouts user from the session

    Variables:
        errors (int): Count number of errors

    Returns:
        (bool): Returns true if no error occurs during the operation otherwise returns false.

    Raises:
        UsernameNotInSession: If username is not present in session.

    """

    errors = 0

    try:
        if "username" not in session:
            raise UsernameNotInSession

        username = session["username"]
        print(f"{username = } logged out from session")
        session.clear()

    except UsernameNotInSession as err:
        errors += 1
        err.print_error()

    except (Exception, psycopg2.Error) as err:
        errors += 1
        bcolors.print_warning("Logout failed ", repr(err))

    finally:
        if errors:
            return False

        return True


def get_user_by_username(username: str) -> User | Literal[False]:
    """Returns user

    Args:
        username (str): Username query

    Variables:
        user (User): Stores User object

    Returns:
        user (User): User object
        Literal[False]: If error occures

    Raise:
        UsernameError: Raises if username is not present in database

    """
    try:
        user: User = User.query.filter_by(username=username).first()
        print(
            {
                "id": user.id,
                "name": user.username,
                "role": user.role,
            }
        )

        if not user:
            raise UsernameError

        return user

    except UsernameError as err:
        err.print_error()
        return False

    except (Exception, psycopg2.Error) as err:
        bcolors.print_warning("Get user by username operation failed ", repr(err))
        return False


def update_user_by_username(username: str) -> bool:
    """Updates user

    Args:
        username (str): Username query

    Variables:
        user (User): Stores User object

    Returns:
        _check (bool): Returns whetere user is updated

    Raise:
        UsernameError: Raises if username is not present in database
        PasswordError: Raises if password does not matches database password

    """

    _check = False

    try:
        user: User = User.query.filter_by(username=username).first()
        password = get_form_data("password")
        new_role = get_form_data("new_role", required=True)
        role_validator(new_role)

        if not user:
            raise UsernameError

        if not citenote_check_hash(password, user.password):
            raise PasswordError

        user.role = new_role
        db.session.commit()

        _check = True

    except (UsernameError, PasswordError) as err:
        err.print_error()
        _check = False

    except (Exception, psycopg2.Error) as err:
        print("Get user by username operation failed ", err)
        _check = False

    finally:
        return _check


if __name__ == "__main__":
    ...
