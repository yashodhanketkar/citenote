import json
from ..models.users import db as user_db
from ..models.data_models import db as dtm_db


def get_uri():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    user = config["pg_user"]
    password = config["pg_password"]
    host = config["pg_host"]
    port = config["pg_port"]
    database = config["pg_database"]

    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def init_dbs(_app):
    user_db.init_app(_app)
    dtm_db.init_app(_app)


if __name__ == "__main__":
    print(get_uri())
