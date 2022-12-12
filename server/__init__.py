from flask import Flask
from .util import set_config as config
from .routes import home, users
from .util.helper import create_admin, init_db
from .util.logger import logger_citenote


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.after_request(logger_citenote)
    app.cli.add_command(init_db)
    app.cli.add_command(create_admin)

    with app.app_context():
        config.configure()

    @app.route("/")
    def root():
        return {"/root": app.root_path}, 200

    app.register_blueprint(home._home)
    app.register_blueprint(users._users)

    return app
