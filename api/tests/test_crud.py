import pytest
from app import app, db
from DB.models import User
from DB.dbHandler import generate_id


@pytest.fixture
def test_client():
    flask_app = app
    flask_app.config["TESTING"] = True

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            next_id = generate_id()
            user_1 = get_user_by_email("test_user_1@gmail.com")
            if user_1 is None:
                test_user_1 = User(id=next_id, first_name="test", last_name="user_1", password="10", email="test_user_1@gmail.com")
                db.session.add(test_user_1)
            next_id = generate_id()
            user_2 = get_user_by_email("test_user_2@gmail.com")
            if user_2 is None:
                test_user_2 = User(id=next_id, first_name="test", last_name="user_2", password="10", email="test_user_2@gmail.com")
                db.session.add(test_user_2)
            db.session.commit()
            yield testing_client


#### SUCCESS TESTS ####


# create 2 users for test and print them to output.txt
def test_create_users(test_client):
    data_1 = {"first_name": "Terry", "last_name": "Jeffords", "password": "10", "email": "Terry@gmail.com"}
    data_2 = {"first_name": "Charles", "last_name": "Boyle", "password": "11", "email": "Charles@gmail.com"}
    response = test_client.post('/user', json=data_1)
    assert response.status_code == 201
    user_id = get_user_id(response)
    print_user_to_file(test_client, user_id)
    response = test_client.post('/user', json=data_2)
    assert response.status_code == 201
    user_id = get_user_id(response)
    print_user_to_file(test_client, user_id)


# get user details by id
def test_get_user(test_client):
    user = get_user_by_email("test_user_1@gmail.com")
    response = test_client.get(f'/user/{user.id}')
    assert response.status_code == 200


# update existing user details
def test_update_user(test_client):
    data = {"first_name": "Jake", "last_name": "Peralta", "password": "11", "email": "Jake@gmail.com"}
    user = get_user_by_email("test_user_1@gmail.com")
    response = test_client.put(f'/user/{user.id}', json=data)
    assert response.status_code == 200
    print_user_to_file(test_client, user.id)


# delete existing user
def test_delete_user(test_client):
    user = get_user_by_email("test_user_2@gmail.com")
    response = test_client.delete(f'/user/{user.id}')
    assert response.status_code == 200


#### FAILURE TESTS ####


# create user that already exists in DB
def test_create_existing_user(test_client):
    data = {"first_name": "test", "last_name": "user_2", "password": "11", "email": "test_user_2@gmail.com"}
    response = test_client.post('/user', json=data)
    assert response.status_code == 400


# update user that doesn't exist in DB
def test_update_non_existing_user(test_client):
    data = {"first_name": "Jake", "last_name": "Peralta", "password": "11", "email": "Jake@gmail.com"}
    next_id = generate_id()
    response = test_client.put(f'/user/{next_id}', json=data)
    assert response.status_code == 400


# delete user that doesn't exist in DB
def test_delete_non_existing_user(test_client):
    next_id = generate_id()
    response = test_client.delete(f'/user/{next_id}')
    assert response.status_code == 400


# get user that doesn't exist in DB
def test_get_non_existing_user(test_client):
    next_id = generate_id()
    response = test_client.get(f'/user/{next_id}')
    assert response.status_code == 400
    delete_remaining_users()


# delete all remaining users in db
def delete_remaining_users():
    users_emails = ["test_user_1@gmail.com", "test_user_2@gmail.com", "Terry@gmail.com", "Charles@gmail.com", "Jake@gmail.com"]
    for user_email in users_emails:
        user = User.query.filter_by(email=user_email.lower()).first()
        if user:
            db.session.delete(user)
            db.session.commit()


# get user id from response message
def get_user_id(response):
    user = response.get_json()
    user_id = user['message']['id']
    return user_id


def get_user_by_email(email_addr):
    user = User.query.filter_by(email=email_addr.lower()).first()
    return user


# print created users to output.txt
def print_user_to_file(test_client, id):
    response = test_client.get(f'/user/{id}')
    data = response.get_json()
    with open('logs/output.log', 'a') as f:
        if 'Jake' not in str(data):
            f.write("users created:\n" + f'id={id}' + str(data) + '\n')
        else:
            f.write("users updated:\n" + f'id={id}' + str(data) + '\n')

