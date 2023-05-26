from flask import Flask, request, jsonify, make_response
from DB.models import User
from app import db


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
            return make_response(jsonify({'message': 'Error! ID already exists'}), 400)
        elif 'duplicate key value violates unique constraint "users_email_key"' in error_message:
            return make_response(jsonify({'message': 'Error! Email already exists'}), 400)
        return make_response(jsonify({'message': 'ERROR!'}), 500)


# get user by id from DB
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'user': user.json()}), 200)
        return make_response(jsonify({'message': 'ERROR! user not found'}), 400)
    except Exception as e:
        return make_response(jsonify({'message': 'ERROR!'}), 500)


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
        return make_response(jsonify({'message': 'ERROR! user id not found'}), 400)
    except Exception as e:
        db.session.rollback()
        error_message = str(e.orig)
        if 'duplicate key value violates unique constraint "users_pkey"' in error_message:
            return make_response(jsonify({'message': 'Error! ID already exists'}), 400)
        elif 'duplicate key value violates unique constraint "users_email_key"' in error_message:
            return make_response(jsonify({'message': 'Error! Email already exists'}), 400)
        return make_response(jsonify({'message': 'ERROR!'}), 500)


# delete user
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': user.json()['id']}), 200)
        return make_response(jsonify({'message':'ERROR! user not found'}), 400)
    except Exception as e:
        return make_response(jsonify({'message':'ERROR!'}), 500)