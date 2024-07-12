"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Like, Post, Comment
from flask_bcrypt import Bcrypt


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql://noah:Godalone1.@localhost:5432/Capstone_one_basketball_test"
bcrypt = Bcrypt()


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

# db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        self.users = []
        self.posts = []

        u1 = User(
            username="t1",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.commit()

        self.users.append(u1)

        u2 = User(
            username="t2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u2)
        db.session.commit()

        self.users.append(u2)

    def tearDown(self):
        for post in self.posts:
            db.session.delete(post)
        for user in self.users:
            db.session.delete(user)

        db.session.commit()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            username="t",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()
        self.users.append(u)

        # User should have no messages & no followers
        self.assertEqual(len(u.posts), 0)

    def test_posts(self):

        p1=Post(
            username="t1",
            title="p1",
            content="c1"
        )
        db.session.add(p1)
        db.session.commit()
        
        self.assertEqual(len(self.users[0].posts), 1)

        db.session.delete(p1)
        db.session.commit()
