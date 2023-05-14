from os import environ
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
db = SQLAlchemy(app)

from DB.models import User

with app.app_context():
    db.create_all()


@app.route("/")
def hello():
    return "Hello World!?!?!?!?"


# add user
@app.route("/users", methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(id=data['id'], first_name=data['first_name'],
                        last_name=data['last_name'], password=data['password'],
                        email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'user created!'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'ERROR!'}), 500)
    

#get all users
@app.route("/users", methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify({'users': [user.json() for user in users]}),200)
    except Exception as e:
        return make_response(jsonify({'message': 'ERROR!'}), 500)


#update user
@app.route("/users/<int:id>", methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.password = data['password']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message': 'user updated!'}), 200)
        return make_response(jsonify({'message': 'ERROR! user id not found'}), 500)
    except Exception as e:
        return make_response(jsonify({'message', 'ERROR!'}), 500)
    
#delete user
@app.route("/users/<int:id>", methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message':'user deleted!'}), 200)
        return make_response(jsonify({'message':'ERROR! user not found'}), 500)
    except Exception as e:
        return make_response(jsonify({'message':'ERROR!'}), 500)