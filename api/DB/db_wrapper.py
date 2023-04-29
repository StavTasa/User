from os import environ
from flask_sqlalchemy import SQLAlchemy


class DBWrapper:
    def __init__(self):
        self.db = SQLAlchemy()

    def connect_to(self, app):
        app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
        self.db.init_app(app)
