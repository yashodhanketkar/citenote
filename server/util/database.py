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
    print("Connected to db")
    return g.db


def close_db():
    print("Disconnected from db")
    if g.db:
        g.db.close()


def init_db():
    print("Initiated database")
    cursor = g.db.cursor()
    with open(r"server/models/users.sql", "r") as query_file:
        cursor.execute(query_file.read())
    g.db.commit()
    cursor.close()


def connect_db(bp):
    @bp.before_request
    def before_request():
        g.db = get_db()

    @bp.teardown_request
    def teardown_request(res):
        close_db()
        return res
