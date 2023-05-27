import pytest
from app import app, db
from DB.models import User

@pytest.fixture
def test_client():
    flask_app = app
    flask_app.config["TESTING"] = True
    
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            user_1 = User.query.filter_by(id="1").first()
            if user_1 is None:
                test_user_1 = User(id=1, first_name="test", last_name="user_1", password="10", email="test_user_1@gmail.com")
                db.session.add(test_user_1)
            
            user_2 = User.query.filter_by(id="2").first()
            if user_2 is None:
                test_user_2 = User(id=2, first_name="test", last_name="user_2", password="10", email="test_user_2@gmail.com")
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
    print_user_to_file(test_client, 3)
    response = test_client.post('/user', json=data_2)
    assert response.status_code == 201
    print_user_to_file(test_client, 4)


# get user details by id
def test_get_user(test_client):
    response = test_client.get('/user/1')
    assert response.status_code == 200


# update existing user details
def test_update_user(test_client):
    data = {"first_name": "Jake", "last_name": "Peralta", "password": "11", "email": "Jake@gmail.com"}
    response = test_client.put('/user/1', json=data)
    assert response.status_code == 200
    print_user_to_file(test_client, 1)


# delete existing user
def test_delete_user(test_client):
    response = test_client.delete('/user/3')
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
    response = test_client.put('/user/14', json=data)
    assert response.status_code == 400


# delete user that doesn't exist in DB
def test_delete_non_existing_user(test_client):
    response = test_client.delete('/user/14')
    assert response.status_code == 400


# get user that doesn't exist in DB
def test_get_non_existing_user(test_client):
    response = test_client.get('/user/14')
    assert response.status_code == 400
    delete_remaining_users()


# delete all remaining users in db
def delete_remaining_users():
    for i in range(1, 5):
        user = User.query.filter_by(id=i).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            with open('logs/output.log', 'a') as f:
                f.write("deleted all users\n")


# print created users to output.txt
def print_user_to_file(test_client, id):
    response = test_client.get(f'/user/{id}')
    data = response.get_json()
    with open('logs/output.log', 'a') as f:
        if 'Jake' not in str(data):
            f.write("users created:\n" + f'id={id}' + str(data) + '\n')
        else:
            f.write("users updated:\n" + f'id={id}' + str(data) + '\n')
