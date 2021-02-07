"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        user = User.signup(
            email="test@test.test",
            username="testuser",
            password="TESTPASSWORD"
        )

        db.session.add(user)
        db.session.commit()

        self.user = User.query.filter_by(username="testuser").first()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        self.assertEqual(len(self.user.messages), 0)
        self.assertEqual(len(self.user.followers), 0)
        self.assertEqual(len(self.user.following), 0)

    def test_user_repr(self):
        """Does the repr method word as expected?"""

        self.assertEqual(repr(
            self.user),
            f"<User #{self.user.id}: {self.user.username}, {self.user.email}>")

    def test_user_is_following(self):
        # when followed, does it show that user is following user2
        user2 = User(
            email="test2@test.test",
            username="testuser2",
            password="TESTPASSWORD2")

        db.session.add(user2)
        db.session.commit()

        user2 = User.query.filter_by(username="testuser2").first()

        self.user.following.append(user2)
        self.assertTrue(self.user.is_following(user2))

        # after un-following, does it show that user is not following user2
        self.user.following.remove(user2)
        self.assertFalse(self.user.is_following(user2))

    def test_user_is_followed_by(self):

        user2 = User(
            email="test2@test.test",
            username="testuser2",
            password="TESTPASSOWRD2"
        )

        db.session.add(user2)
        db.session.commit()

        user2 = User.query.filter_by(username="testuser2").first()

        user2.following.append(self.user)
        db.session.add(user2)
        db.session.commit()
        self.assertTrue(self.user.is_followed_by(user2))

        user2.following.remove(self.user)
        db.session.add(user2)
        db.session.commit()
        self.assertFalse(self.user.is_followed_by(user2))

    def test_user_authenticated(self):

        self.assertTrue(User.authenticate(self.user.username, "TESTPASSWORD"))

        self.assertFalse(User.authenticate(
            self.user.username, "BADPASSWORD"))

        authentication_return = User.authenticate('testuser', 'TESTPASSWORD')

        self.assertEqual(
            type(authentication_return),
                User)

    def test_user_bad_password_signup(self):
        pass
