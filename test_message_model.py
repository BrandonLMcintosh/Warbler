from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows

# Does the repr method work as expected?
# Does is_following successfully detect when user1 is following user2?
# Does is_following successfully detect when user1 is not following user2?
# Does is_followed_by successfully detect when user1 is followed by user2?
# Does is_followed_by successfully detect when user1 is not followed by user2?
# Does User.create successfully create a new user given valid credentials?
# Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
# Does User.authenticate successfully return a user when given a valid username and password?
# Does User.authenticate fail to return a user when the username is invalid?
# Does User.authenticate fail to return a user when the password is invalid?

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

db.create_all()

class MessageModelTestCase(TestCase):

    def setUp(self):

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        User.signup(
            email="test@test.test",
            username="testuser",
            password="TESTPASSWORD"
        )

        msg1 = Message(text="test1")
        msg2 = Message(text="test2")
        msg3 = Message(text="test3")


        self.user = User.query.filter_by(username='testuser').first()

        self.user.messages.append(msg1)
        self.user.messages.append(msg2)
        self.user.messages.append(msg3)

        db.session.add(self.user)
        db.session.commit()

        self.client = app.test_client()

    def test_message_model(self):
        self.assertEqual(len(self.user.messages), 3)

    def test_message_repr(self):
        self.assertEqual(repr(self.user.messages[0]), "test1")

    def test_message_likes(self):
        User.signup(
            email="test2",
            username="testuser2",
            password="TESTPASSWORD2"
        )

        user2 = User.query.filter_by(username="testuser").first()

        user2.likes.append(self.user.messages[0])

        db.session.commit()

        self.assertEqual(len(user2.likes), 1)
        self.assertEqual(repr(user2.likes[0]), "test1")