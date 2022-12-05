from flask import Flask
from .util import set_config as config
from .routes import home, users


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    with app.app_context():
        config.configure()

    @app.route("/")
    def root():
        return {"/root": app.root_path}, 200

    app.register_blueprint(home._home)
    app.register_blueprint(users._users)

    return app
