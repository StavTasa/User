import pytest
from app import app, db
from DB.models import User

@pytest.fixture
def test_client():
    flask_app = app
    flask_app.config["TESTING"] = True
    
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
            # after test finished delete remaining user
            user = User.query.filter_by(id=11).first()
            if user:
                db.session.delete(user)
                db.session.commit()


#### SUCCESS TESTS ####


# create 2 users for test and print them to output.txt
def test_create_users(test_client):
    data_1 = {"id": "10", "first_name": "Terry", "last_name": "Jeffords", "password": "10", "email": "Terry@gmail.com"}
    data_2 = {"id": "11", "first_name": "Charles", "last_name": "Boyle", "password": "11", "email": "Charles@gmail.com"}
    response = test_client.post('/user', json=data_1)
    assert response.status_code == 201
    print_user_to_file(test_client, 10)
    response = test_client.post('/user', json=data_2)
    assert response.status_code == 201
    print_user_to_file(test_client, 11)


# get user details by id
def test_get_user(test_client):
    response = test_client.get('/user/10')
    assert response.status_code == 200


# update existing user details
def test_update_user(test_client):
    data = {"id": "10", "first_name": "Jake", "last_name": "Peralta", "password": "11", "email": "Jake@gmail.com"}
    response = test_client.put('/user/10', json=data)
    assert response.status_code == 200
    print_user_to_file(test_client, 10)


# delete existing user
def test_delete_user(test_client):
    response = test_client.delete('/user/10')
    assert response.status_code == 200


#### FAILURE TESTS ####


# create user that already exists in DB
def test_create_existing_user(test_client):
    data = {"id": "11", "first_name": "Charles", "last_name": "Boyle", "password": "11", "email": "Charles@gmail.com"}
    response = test_client.put('/user/11', json=data)
    assert response.status_code == 400


# update user that doesn't exist in DB
def test_update_non_existing_user(test_client):
    data = {"id": "10", "first_name": "Jake", "last_name": "Peralta", "password": "11", "email": "Jake@gmail.com"}
    response = test_client.put('/user/10', json=data)
    assert response.status_code == 400


#delete user that doesn't exist in DB
def test_delete_non_existing_user(test_client):
    response = test_client.delete('/user/10')
    assert response.status_code == 400


# get user that doesn't exist in DB
def test_get_non_existing_user(test_client):
    response = test_client.get('/user/10')
    assert response.status_code == 400


# print created users to output.txt
def print_user_to_file(test_client, id):
    response = test_client.get(f'/user/{id}')
    data = response.get_json()
    with open('logs/output.log', 'a') as f:
        if 'Jake' not in str(data):
            f.write("users created:\n" + str(data) + '\n')
        else:
            f.write("users updated:\n" + str(data) + '\n')
