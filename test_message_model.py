"""Messsage model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py

import os
from unittest import TestCase
from models import db, User, Message, Follows, Like

os.environ['DATABASE_URL'] = "postgresql:///meowchat-test"

from app import app

db.create_all()

class MessageModelTestCase(TestCase):
    """Test Message""" 

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_message_model(self):

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.commit()

        m1 = Message(
            text="hello",
            user_id=u1.id, 
            )

        db.session.add(m1)
        db.session.commit()

        self.assertTrue(m1 in u1.messages)

