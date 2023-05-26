from flask import Flask, request, jsonify, make_response
from DB.dbHandler import create_user, get_user, update_user, delete_user
from app import app


# Create a user
@app.route("/user", methods=['POST'])
def create_user_route():
    data = request.get_json()
    result = create_user(data)
    return result


@app.route("/user/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def handle_user_route(id):
    if request.method == 'GET':
        # Get a user by ID
        result = get_user(id)
        return result

    elif request.method == 'PUT':
        # Update a user
        data = request.get_json()
        result = update_user(id, data)
        return result

    elif request.method == 'DELETE':
        # Delete a user
        result = delete_user(id)
        return result
