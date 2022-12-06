import click
import json
import secrets

import psycopg2
import getpass

from .database import get_db, close_db
from flask import g
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash


def validate_superuser(user):
    if user == config["pg_user"]:
        password = getpass.getpass()
        if password == config["pg_password"]:
            return True
    return False


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


with open("config.json") as config_file:
    config = json.load(config_file)


def citenote_gen_hash(password: str) -> (str, str):
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
            raise psycopg2.errors.InvalidAuthorizationSpecification

        get_db()
        cursor = g.db.cursor()

        if force:
            captcha = secrets.token_hex(3)
            verify_captcha = input(f"Please enter this '{captcha}':\n")

            if captcha != verify_captcha:
                raise Exception("Invalid captcha")

            print("Captcha verified")

            with open(r"server/models/citenote_clean.sql", "r") as query_file:
                cursor.execute(query_file.read())

            print("Force initiated database")

        else:
            print("Initiated database")

        with open(r"server/models/citenote.sql", "r") as query_file:
            cursor.execute(query_file.read())

        g.db.commit()
        bcolors.print_success("Database initiated.")

    except psycopg2.errors.InvalidAuthorizationSpecification:
        bcolors.print_warning("Authentication failed", "InvalidAuthorizationSpecification")

    except psycopg2.errors.DuplicateTable:
        message = "Database is already initiated."
        error = "DuplicateTable"
        bcolors.print_warning(message, error)

    except (Exception, psycopg2.Error) as err:
        bcolors.print_warning("Some error occurred during database creation.", err)

    finally:
        if "db" in g:
            cursor.close()
            close_db()


@click.command("create-admin")
@click.option("-u", "--user")
@with_appcontext
def create_admin(user):
    try:
        if not validate_superuser(user):
            raise psycopg2.errors.InvalidAuthorizationSpecification
        get_db()
        create_admin_query = """
        insert into users (id, username, password, role)
        Values (%s, %s, %s, %s);
        """
        password = citenote_gen_hash("admin")
        admin_default = (9999, "admin", password, "admin")
        cursor = g.db.cursor()
        cursor.execute(create_admin_query, admin_default)
        g.db.commit()
        bcolors.print_success("User admin created!!")

    except psycopg2.errors.InvalidAuthorizationSpecification:
        bcolors.print_warning("Authentication failed", "InvalidAuthorizationSpecification")

    except psycopg2.errors.UniqueViolation:
        bcolors.print_warning("User admin already exists", "UniqueViolation")

    except (Exception, psycopg2.Error) as err:
        bcolors.print_warning("Some error occurred during admin creation.", err)

    finally:
        if "db" in g:
            cursor.close()
            close_db()
