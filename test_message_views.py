"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///meowchat-test"

# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

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

    def test_add_message(self):
        """Can use add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.filter_by(text="Hello").first()
            self.assertEqual(msg.text, "Hello")

    def test_message_show(self):
        "Can we show a message?"

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.get(f"messages/{self.testmessage.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.testmessage.text, html)
    
    def test_messages_destroy(self):
        """ Can we delete a message"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
        
            resp = c.post(f"/messages/{self.testmessage.id}/delete")
            user = User.query.get(self.testuser.id)

            self.assertEqual(resp.status_code, 302)
            self.assertFalse(user.messages)
        
        
    def test_liking(self):
        """can we like a message?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            user2 = User.signup(username="user2",
                                email="user2@user2.com",
                                password="password2",
                                image_url=None)
                                
            db.session.commit()

            message2 = Message(text="yet another message")
            user2.messages.append(message2)
            
            db.session.commit()
            
            resp = c.post(f"/liking/{message2.id}")
            user = User.query.get(self.testuser.id)

            self.assertTrue(message2 in user.messages_user_likes)
