"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


from app import app, CURR_USER_KEY
import os
from unittest import TestCase

from models import db, connect_db, Message, User, Like

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///meowchat-test"

# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        db.session.commit()

        self.testuser = User.query.filter_by(username="testuser").first()
        self.testmessage = Message(text="another message")
        self.testuser.messages.append(self.testmessage)

        db.session.commit()

        self.testmessage = Message.query.filter_by(text="another message").first()

    def test_show_users(self):  
        """Can we show a user?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f"users/{self.testuser.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.testuser.username, html)

    # def test_show_following(self):
    #     """can we test a following"""

    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id

    #         user2 = User.signup(username="testuser2",
    #                             email="test2@test.com",
    #                             password="123456",
    #                             image_url=None)
                                    
    #         db.session.commit()
    #         user = User.query.get(self.testuser.id)

    #         user.is_following(user2)

    #         db.session.commit()

    #         resp = c.get(f"/users/{user.id}/following")
    #         html = resp.get_data(as_text=True)

    #         self.assertIn(user2.username, html)
