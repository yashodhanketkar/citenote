from typing import Tuple

from flask import Flask

from .routes import home, manuscripts, papers, users
from .util import set_config as config
from .util.db import init_dbs
from .util.helper import create_admin, init_db
from .util.logger import logger_citenote


def error_handler(err: int) -> Tuple[dict, int]:
    status, message = str(err)[:3], str(err)[4:]
    status = int(status)
    return {
        "status": status,
        "message": message,
    }, status


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.after_request(logger_citenote)

    app.register_error_handler(401, error_handler)
    app.register_error_handler(404, error_handler)

    app.cli.add_command(init_db)
    app.cli.add_command(create_admin)

    with app.app_context():
        config.configure()

    init_dbs(app)

    app.register_blueprint(home._home)
    app.register_blueprint(users._users)
    app.register_blueprint(manuscripts._manuscripts)
    app.register_blueprint(papers._papers)

    return app
