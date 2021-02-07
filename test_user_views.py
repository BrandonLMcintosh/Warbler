from app import CURR_USER_KEY, app
import os
from unittest import TestCase
from models import db, User, Message, Follows

# When you’re logged in, can you see the follower / following pages for any user?
# When you’re logged out, are you disallowed from visiting a user’s follower / following pages?
# When you’re logged in, can you add a message as yourself?
# When you’re logged in, can you delete a message as yourself?
# When you’re logged out, are you prohibited from adding messages?
# When you’re logged out, are you prohibited from deleting messages?
# When you’re logged in, are you prohibiting from adding a message as another user?
# When you’re logged in, are you prohibiting from deleting a message as another user?

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
app.config['WTF_CSRF_ENABLED'] = False

class UserViewsTestCase(TestCase):

    def setUp(self):
        
        db.drop_all()
        db.create_all()

        self.user1 = User.signup(
            email="test1",
            username="test1",
            password="test1"
        )

        self.user2 = User.signup(
            email="test2",
            username="test2",
            password="test2"
        )

        for user in [self.user1, self.user2]:
            for num in range(3):
                user.messages.append(Message(text=f'test_message_{num}'))
        
            db.session.add(user)

        db.session.commit()

        self.client = app.test_client()

    
    def test_see_followers(self):
        with self.client.session_transaction() as session:
            #logged in
            session[CURR_USER_KEY] = self.user1.id
            response = self.client.get('/users/2/followers')
            html = response.get_data(as_text=True)
            self.assertNotIn("Redirecting", html)
            
            #logged out
            del session[CURR_USER_KEY]
            response = self.client.get('/users/2/followers')    
            html = response.get_data(as_text=True)
            self.assertIn("Redirecting", html)

    def test_see_following(self):
        with self.client.session_transaction() as session:
            #logged in
            session[CURR_USER_KEY] = self.user1.id
            response = self.client.get('/users/2/following')
            html = response.get_data(as_text=True)
            self.assertNotIn("Redirecting", html)

            #logged out
            del session[CURR_USER_KEY]
            self.client.allow_subdomain_redirects = True
            response = self.client.get('/users/2/following')
            html = response.get_data(as_text=True)
            self.assertIn("Redirecting", html)


