"""./server/util/set_config

This modules generates the neccessary configurations for the flask application
"""

import secrets
from pathlib import Path

from flask import current_app

from .db import get_uri


def configure():
    """Make configuration for the flask app"""

    _instance_folder = Path(current_app.root_path).joinpath("instance")
    _config_file = Path(_instance_folder).joinpath("config.py")

    # To maintain order of return message
    current_app.config["JSON_SORT_KEYS"] = False

    def get_token():
        """Generates token for the flask app"""
        return secrets.token_hex(32)

    def make_instance_folder():
        """Creates instance folder for flask app"""
        if not Path.is_dir(_instance_folder):
            print("Creating instance folder")
            Path.mkdir(_instance_folder)

    def write_config():
        """Write configuration lines"""

        with _config_file.open(mode="w", encoding="utf-8") as file:
            file.write(f'SECRET_KEY = "{get_token()}"\n')

    def make_config_file(update=False):
        """Creates and updates configuration files for flask app"""

        if not Path.is_file(_config_file) or update:
            write_config()
            if not update:
                print("Writing config file")
            else:
                print("Updating config file")

    def __main__():
        """Calls functions to generate instance folder and config file."""

        make_instance_folder()
        make_config_file()
        current_app.config.from_pyfile(str(_config_file), silent=True)
        current_app.config["SQLALCHEMY_DATABASE_URI"] = get_uri()

    __main__()
