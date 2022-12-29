import configparser
import getpass
import json
import pickle
import secrets

import click
import psycopg2
import psycopg2.errors as pgerr
from flask import g, request
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash

from ...models.data_models import Manuscript, Paper
from ...models.data_models import db as dtm_db
from ...models.users import User
from ...models.users import db as user_db
from ..database import close_db, get_db


def load_config() -> dict:
    """Loads configuration file

    variable:
        config_file (Wrapper): Holds value of configuration file.

    Returns:
        config (dict): Configuration dictionary.

    """
    with open("config.json") as config_file:
        config = json.load(config_file)

    return config


def get_config(key: str) -> str:
    """Get configuration value

    Args:
        key (str): Name of configuration field

    Variables:
        config (ParserObject): Parser for configuration file.

    Returns:
        (str): Value of the configuration field

    """
    config = configparser.ConfigParser()
    config.read("setup.cfg")
    return config.get("metadata", key)


def get_version() -> str:
    """Get current version of application

    Variables:
        version_file (Wrapper): Hold value of VERSION file.

    Returns:
        version (str): Latest version of citenote application.

    """

    with open("VERSION", "r") as version_file:
        version = version_file.read()
    return version


class bcolors:
    """Batch shell/Console Colors

    Hold the text color values for batch shell/console.

    Attributes:
        WARNING (str): Red color for errors/major warnings.
        SUCCESS (str): Green color for success.
        MESSAGE (str): Yellow color for message/minor warnings.
        RESET (str): White color for regular messages and reset colors.

    """

    WARNING = "\u001b[31m"
    SUCCESS = "\u001b[32m"
    MESSAGE = "\u001b[33m"
    RESET = "\u001b[0m"

    @staticmethod
    def print_warning(message="", error=""):
        """Print warning

        Print red colored text for major warning and errors

        Args:
            message (str) = Message provided or ""
            message (str) = Error provided or ""
        """
        print(f"{bcolors.WARNING}{message}\nError: {error}{bcolors.RESET}")

    @staticmethod
    def print_message(message="", status=""):
        """Print message

        Print yellow colored text for minor warning and status.

        Args:
            message (str) = Message provided or ""
            status (str) = Status provided or ""
        """
        status_string = f"({status}) -> " if status else ""
        print(f"{bcolors.MESSAGE}Status: {status_string}{message}{bcolors.RESET}")

    @staticmethod
    def print_success(message=""):
        """Print sucess

        Print green colored text. Used to print message for successfull operation.

        Args:
            message (str) = Message provided or ""
        """
        print(f"{bcolors.SUCCESS}{message}{bcolors.RESET}")


def get_citenote_data(query):
    """Get data from query

    Args:
        query (str): Name of query object.

    Variables:
        data_file (Wrapper): Holds value of data file.

    Returns:
        _val (any): Value of query object.

    """
    with open(r"server/.citenote", "rb") as data_file:
        _val = pickle.load(data_file)[query]

    return _val


def get_form_data(field, required=False, type="TEXT"):
    """Get data from form

    Args:
        field (str): Name of field object.
        required (bool): Is field required.
        type (str): Type of field in datbase (Not yet implemented)

    Returns:
        (str): Value of form object if provided or "".

    Raises:
        ValueError: If required value is not provided (Handles KeyError and raise this exception)

    """
    try:
        return request.form[field]

    except KeyError:
        if required:
            raise ValueError

        return ""


def validate_superuser(user):
    """Validates if superuser requesting access

    Args:
        user (str): Username provided

    Variables:
        password (str): Password provided through shell/console

    Returns:
        (bool): True if superuser is validated else False

    """
    config = load_config()

    if user == config["pg_user"]:
        password = getpass.getpass("Please enter database admin password: ")

        if password == config["pg_password"]:
            return True

    return False


def get_password():
    """Get password via shell/console

    Variables:
        _password (str): Password from user
        _password_cnf (str): Password confirmation from user

    Returns:
        _password (str): _password if provided else "admin"

    """
    _password = getpass.getpass("Enter new password (admin): ")
    _password_cnf = getpass.getpass("Confirm password: ")

    if _password != _password_cnf:
        print("Passwords do not match. Try again\n")
        return get_password()

    if _password == "":
        return "admin"

    return _password


def citenote_gen_hash(password: str) -> str:
    """Generate password hash for citenote application

    Args:
        password (str): Password provided for hashing

    Variables:
        config (dict): Hold application configurations
        pepper (str): Pepper to pepper password before hashing
        peppered_password (str): Plain password after peppering

    Returns:
        (str): Hashed slat-peppered password

    """

    config = load_config()
    pepper = config["pepper"]
    peppered_password = password + pepper

    return generate_password_hash(peppered_password)


def citenote_check_hash(password: str, hash: str) -> bool:
    """Check password hash for citenote application

    Args:
        password (str): Password provided for checking
        hash (str): Password hash provided for checking

    Variables:
        config (dict): Hold application configurations
        pepper (str): Pepper to pepper password before hashing
        peppered_password (str): Plain password after peppering

    Returns:
        (bool): True if hash and peppered_passowrd matches else false.

    """
    config = load_config()
    pepper = config["pepper"]
    peppered_password = password + pepper

    return check_password_hash(hash, peppered_password)


def connect_db(bp):
    """Connects to database (depr)"""

    @bp.before_request
    def before_request():
        """Get database before request is processed"""
        g.db = get_db()

    @bp.teardown_request
    def teardown_request(res):
        """Close database after request is processed"""
        close_db()
        return res


@click.command("init-db")
@click.option("-f", "--force", is_flag=True, show_default=True, default=False, help="Creates database.")
@click.option("-u", "--user")
@with_appcontext
def init_db(force, user):
    """Inits database for flask application

    Creates database from shell/console.

    Args:
        force (bool): True if provided else false
        user (str): Username provided via shell/console

    Variables:
        captcha (str): Get six character random token.
        verify_captcha (str): Hold captcha entered by user.

    Raises:
        InvalidAuthorizationSpecification: If superuser validation fails.
        Exception("Invalid captcha"): Raise if user entered captch does not matches generated captcha.

    """
    try:
        if not validate_superuser(user):
            raise pgerr.InvalidAuthorizationSpecification

        if force:
            captcha = secrets.token_hex(3)
            verify_captcha = input(f"Please enter this '{captcha}':\n")

            if captcha != verify_captcha:
                raise Exception("Invalid captcha")

            print("Captcha verified")
            User.__table__.drop(user_db.engine)
            Paper.__table__.drop(dtm_db.engine)
            Manuscript.__table__.drop(dtm_db.engine)
            # Citation.__table__.drop(dtm_db.engine)
            print("Force initiated database")

        else:
            print("Initiated database")

        user_db.create_all()
        dtm_db.create_all()

        bcolors.print_success("Database initiated.")

    except pgerr.InvalidAuthorizationSpecification:
        bcolors.print_warning("Authentication failed", "InvalidAuthorizationSpecification")

    except pgerr.DuplicateTable:
        message = "Database is already initiated."
        error = "DuplicateTable"
        bcolors.print_warning(message, error)

    except (Exception, psycopg2.Error) as err:
        bcolors.print_warning("Some error occurred during database creation.", repr(err))


@click.command("create-admin")
@click.option("-u", "--user")
@with_appcontext
def create_admin(user):
    """Creates admin user in database

    Creates admin from shell/console.

    Args:
        user (str): Username provided via shell/console
        password (str): Holds password hash.
        admin (User): Admin/Super user.

    Variables:
        captcha (str): Get six character random token.
        verify_captcha (str): Hold captcha entered by user.

    Raises:
        InvalidAuthorizationSpecification: If superuser validation fails.

    """
    try:
        if not validate_superuser(user):
            raise pgerr.InvalidAuthorizationSpecification

        print("Creating 'admin' account.")
        password = citenote_gen_hash(get_password())
        admin = User("admin", password, "admin")
        admin.id = 9999

        user_db.session.add(admin)
        user_db.session.commit()
        bcolors.print_success("User admin created!!")

    except pgerr.InvalidAuthorizationSpecification:
        bcolors.print_warning("Authentication failed", "InvalidAuthorizationSpecification")

    except pgerr.UniqueViolation:
        bcolors.print_warning("User admin already exists", "UniqueViolation")

    except (Exception, psycopg2.Error) as err:
        bcolors.print_warning("Some error occurred during admin creation.", repr(err))
