from flask import Flask, request, jsonify, make_response
from DB.models import User
from app import db
from errors import UserNotFoundError, DuplicateEmailError, DuplicateIDError, DatabaseError


# create new user in db
def create_user(data):
    try:
        new_user = User(id=data['id'], first_name=data['first_name'],
                        last_name=data['last_name'], password=data['password'],
                        email=data['email'].lower())
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': new_user.json()}), 201)
    except Exception as e:
        db.session.rollback()
        error_message = str(e.orig)
        if 'duplicate key value violates unique constraint "users_pkey"' in error_message:
            raise DuplicateIDError()
        elif 'duplicate key value violates unique constraint "users_email_key"' in error_message:
            raise DuplicateEmailError()
        raise DatabaseError()


# get user by id from DB
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'user': user.json()}), 200)
        raise UserNotFoundError()
    except UserNotFoundError:
        raise
    except Exception as e:
        raise DatabaseError()
    

# update user details
def update_user(id, data):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            user.id = data['id']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.password = data['password']
            user.email = data['email'].lower()
            db.session.commit()
            return make_response(jsonify({'message': user.json()}), 200)
        raise UserNotFoundError()
    except UserNotFoundError:
        raise
    except Exception as e:
        db.session.rollback()
        error_message = str(e.orig)
        if 'duplicate key value violates unique constraint "users_pkey"' in error_message:
            raise DuplicateIDError()
        elif 'duplicate key value violates unique constraint "users_email_key"' in error_message:
            raise DuplicateEmailError()
        raise DatabaseError()


# delete user
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': user.json()['id']}), 200)
        raise UserNotFoundError()
    except UserNotFoundError:
        raise
    except Exception as e:
        db.session.rollback()
        raise DatabaseError()