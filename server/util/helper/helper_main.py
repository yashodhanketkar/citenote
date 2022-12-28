import configparser
import getpass
import json
import pickle
import secrets

import click
import psycopg2
import psycopg2.errors as pgerr

from flask import g
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash

from ...models.users import db as user_db, User
from ...models.data_models import db as dtm_db, Paper, Manuscript, Citation
from ..database import close_db, get_db


def get_config(key):
    config = configparser.ConfigParser()
    config.read("setup.cfg")
    return config.get("metadata", key)


def get_version():
    with open("VERSION", "r") as version_file:
        version = version_file.read()
    return version


class bcolors:
    WARNING = "\u001b[31m"
    SUCCESS = "\u001b[32m"
    MESSAGE = "\u001b[34m"
    RESET = "\u001b[0m"

    @staticmethod
    def print_warning(message="", error=""):
        print(f"{bcolors.WARNING}{message}\nError: {error}{bcolors.RESET}")

    @staticmethod
    def print_message(message="", status=""):
        status_string = f"({status}) -> " if status else ""
        print(f"{bcolors.MESSAGE}Status: {status_string}{message}{bcolors.RESET}")

    @staticmethod
    def print_success(message=""):
        print(f"{bcolors.SUCCESS}{message}{bcolors.RESET}")


def get_citenote_data(query):
    with open(r"server/.citenote", "rb") as data_file:
        _val = pickle.load(data_file)[query]

    return _val


def validate_superuser(user):
    if user == config["pg_user"]:
        password = getpass.getpass("Please enter database admin password: ")

        if password == config["pg_password"]:
            return True

    return False


def get_password():
    _password = getpass.getpass("Enter new password (admin): ")
    _password_cnf = getpass.getpass("Confirm password: ")

    if _password != _password_cnf:
        print("Passwords do not match. Try again\n")
        return get_password()

    if _password == "":
        return "admin"

    return _password


with open("config.json") as config_file:
    config = json.load(config_file)


def citenote_gen_hash(password: str) -> str:
    pepper = config["pepper"]
    peppered_password = password + pepper

    return generate_password_hash(peppered_password)


def citenote_check_hash(password: str, hash: str) -> bool:
    pepper = config["pepper"]
    peppered_password = password + pepper

    return check_password_hash(hash, peppered_password)


def connect_db(bp):
    @bp.before_request
    def before_request():
        g.db = get_db()

    @bp.teardown_request
    def teardown_request(res):
        close_db()
        return res


@click.command("init-db")
@click.option("-f", "--force", is_flag=True, show_default=True, default=False, help="Creates database.")
@click.option("-u", "--user")
@with_appcontext
def init_db(force, user):
    try:
        if not validate_superuser(user):
            raise pgerr.InvalidAuthorizationSpecification

        if force:
            captcha = secrets.token_hex(3)
            verify_captcha = input(f"Please enter this '{captcha}':\n")

            if captcha != verify_captcha:
                raise Exception("Invalid captcha")

            print("Captcha verified")
            # User.__table__.drop(user_db.engine)
            Paper.__table__.drop(dtm_db.engine)
            Manuscript.__table__.drop(dtm_db.engine)
            Citation.__table__.drop(dtm_db.engine)
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
        bcolors.print_warning("Some error occurred during database creation.", str(err))


@click.command("create-admin")
@click.option("-u", "--user")
@with_appcontext
def create_admin(user):
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
        bcolors.print_warning("Some error occurred during admin creation.", str(err))


def get_form_data(field, required=False, type="TEXT"):
    try:
        return request.form[field]

    except KeyError:
        if required:
            raise ValueError

        return ""
