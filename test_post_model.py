"""Post model tests."""

# run these tests like:
#
#    python -m unittest test_post_model.py


import os
from unittest import TestCase

from models import db, User, LikeButton, Post, Comment
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

db.create_all()


class PostModelTestCase(TestCase):
    def setUp(self):
        """Create test client, add sample data."""
        db.session.query(User).delete(synchronize_session=False)
        u1 = User(
            username="t1",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.commit()

        p1 = Post(
            username="t1",
            title="blessed virgin",
            content="immaculate conception"
        )

        self.u1 = u1

        u2 = User(
            username="t2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u2)
        db.session.add(p1)
        db.session.commit()

        self.u2 = u2
        self.p1 = p1

    def test_post_model(self):
        """Does basic model work?"""

        p = Post(
            username="t1",
            title="gluttony",
            content="vice that creeps up on you"
        )

        db.session.add(p)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(p.likes, 0)
        self.assertEqual(len(p.comments), 0)

        db.session.delete(self.p1)
        db.session.delete(self.u1)
        db.session.delete(self.u2)
        db.session.delete(p)
        db.session.commit()

    def test_likes(self):
        l = LikeButton(post_username="t1",
                        like_username="t2",
                        post_id=self.p1.id,
                        clicked=True)

        db.session.add(l)
        db.session.commit()

        assertEqual(self.u1.likes, 1)

        db.session.delete(self.p1)
        db.session.delete(self.u1)
        db.session.delete(self.u2)
        db.session.delete(l)
        db.session.commit()