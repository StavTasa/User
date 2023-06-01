from DB.models import User
from sqlalchemy import func
from app import db


class Crud():
    def create_user(data):
        next_id = generate_id()
        new_user = User(id=next_id, first_name=data['first_name'],
                        last_name=data['last_name'], password=data['password'],
                        email=data['email'].lower())
        db.session.add(new_user)
        db.session.commit()
        return new_user

    # get user by id from DB
    def get_user(id):
        user = User.query.filter_by(id=id).first()
        if user:
            return user
        return 'user not found'

    # update user details
    def update_user(id, data):
        user = User.query.filter_by(id=id).first()
        if user:
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.password = data['password']
            user.email = data['email'].lower()
            db.session.commit()
            return user
        return 'user not found'

    def delete_user(id):
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return user
        return 'user not found'


def generate_id():
    max_id = db.session.query(func.max(User.id)).scalar()
    res = (max_id or 0) + 1
    return res
