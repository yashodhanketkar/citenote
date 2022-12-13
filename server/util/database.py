import json

import psycopg2
from flask import g


with open("config.json") as config_file:
    postgres = json.load(config_file)


def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            user=postgres["pg_user"],
            password=postgres["pg_password"],
            host=postgres["pg_host"],
            port=postgres["pg_port"],
            database=postgres["pg_database"],
        )
    return g.db


def close_db():
    if g.db:
        g.db.close()
