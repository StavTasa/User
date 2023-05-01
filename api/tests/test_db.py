import pytest
from app import app, db
from DB.models import User


@pytest.fixture(scope="module")
def test_client():
    flask_app = app
    flask_app.config["TESTING"] = True

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
            # after the test is done, delete the test user record
            test_user = User.query.filter_by(email="testuser@example.com").first()
            if test_user:
                db.session.delete(test_user)
                db.session.commit()


def test_user_db():
    with app.app_context():
        # create a test user
        test_user = User(
            first_name="Jhon",
            last_name="Doe",
            email="testuser@example.com",
            password="bilbo123",
        )
        db.session.add(test_user)
        db.session.commit()

        # check if the user was saved in the db
        saved_user = User.query.filter_by(email="testuser@example.com").first()
        assert saved_user is not None
