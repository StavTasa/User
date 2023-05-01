from os import environ
from DB.models import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
db = SQLAlchemy(app)


with app.app_context():
    db.create_all()


@app.route("/")
def hello():
    return "Hello World!?!?!?!?"
