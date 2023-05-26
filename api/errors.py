from flask import jsonify, make_response
from app import app


class UserNotFoundError(Exception):
    pass


class DuplicateIDError(Exception):
    pass


class DuplicateEmailError(Exception):
    pass


class DatabaseError(Exception):
    pass


# Error handlers
@app.errorhandler(UserNotFoundError)
def handle_user_not_found_error(error):
    return make_response(jsonify({'message': 'ERROR! user id not found'}), 400)


@app.errorhandler(DuplicateIDError)
def handle_duplicate_id_error(error):
    return make_response(jsonify({'message': 'Error! ID already exists'}), 400)


@app.errorhandler(DuplicateEmailError)
def handle_duplicate_email_error(error):
    return make_response(jsonify({'message': 'Error! Email already exists'}), 400)


@app.errorhandler(DatabaseError)
def handle_database_error(error):
    return make_response(jsonify({'message': 'ERROR!'}), 500)