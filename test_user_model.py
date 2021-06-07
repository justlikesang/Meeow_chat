"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///meowchat-test"

# Now we can import app

from app import app

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

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr(self):
        """Does the repr method work as expected?"""

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.commit()  

        id = u1.id      
    
        self.assertEqual(repr(u1), f"<User #{id}: testuser, test@test.com>") 
    
    def test_is_followed_by(self):
        """Does is_following successfully detect when user1 is following user2?"""

        u1 =  User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
        )
        
        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            followers = [u1]
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertTrue(u2.is_followed_by(u1))

    def test_is_following(self):
        """Does is_following successfully detect when user1 is not following user2?"""

        u1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
        )
            
        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            following = [u1]
        )

        
        db.session.add(u2)
        db.session.commit()

        self.assertFalse(u1.is_following(u2))
        self.assertTrue(u2.is_following(u1))

    def test_signup(self):
        """Does User.signup successfully create a new user given valid credentials?"""

        user = User.signup("bob", "a@a", "password", "www.picture.com")

        self.assertEqual(user.username, "bob")
        self.assertNotEqual(user.password, "password")
            # How do we **"unpack" in Python?

    def test_authenticate(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""

        User.signup("bob", "a@a", "password", "www.picture.com")

        self.assertTrue(User.authenticate("bob", "password"))
        self.assertFalse(User.authenticate("hacker", "hacker"))