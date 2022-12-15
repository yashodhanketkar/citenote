from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):  # type: ignore
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self) -> str:
        return f"{self.id}:{self.username}@{self.role}"
