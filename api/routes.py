from flask import request, jsonify, make_response
from DB.dbHandler import Crud
from app import app, db
from DB.dbErrors import handle_errors, UserNotFoundError


# Create a user
@app.route("/user", methods=['POST'])
def create_user_route():
    try:
        data = request.get_json()
        result = Crud.create_user(data)
        return make_response(jsonify({'message': result.json()}), 201)
    except Exception as e:
        db.session.rollback()
        error_message = str(e.orig)
        handle_errors(error_message)


@app.route("/user/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def handle_user_route(id):
    if request.method == 'GET':
        # Get a user by ID
        try:
            result = Crud.get_user(id)
            if result != 'user not found':
                return make_response(jsonify({'user': result.json()}), 200)
            raise UserNotFoundError()
        except UserNotFoundError:
            raise
        except Exception as e:
            db.session.rollback()
            error_message = str(e.orig)
            handle_errors(error_message)

    elif request.method == 'PUT':
        # Update a user
        try:
            data = request.get_json()
            result = Crud.update_user(id, data)
            if result != 'user not found':
                return make_response(jsonify({'message': result.json()}), 200)
            raise UserNotFoundError()
        except UserNotFoundError:
            raise
        except Exception as e:
            db.session.rollback()
            error_message = str(e.orig)
            handle_errors(error_message)

    elif request.method == 'DELETE':
        # Delete a user
        try:
            result = Crud.delete_user(id)
            if result != 'user not found':
                return make_response(jsonify({'message': result.json()['id']}), 200)
            raise UserNotFoundError()
        except UserNotFoundError:
            raise
        except Exception as e:
            db.session.rollback()
            error_message = str(e.orig)
            handle_errors(error_message)
