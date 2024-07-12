"""Post model tests."""

# These test should be run locally. Adjust test database url as needed.
# run these tests like:
#
#    python -m unittest test_post_model.py


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

db.create_all()


class PostModelTestCase(TestCase):
    def setUp(self):
        """Create test client, add sample data."""
        self.users = []
        self.posts = []
        self.likes = []
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

        self.users.append(u1)

        u2 = User(
            username="t2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u2)
        db.session.add(p1)
        db.session.commit()

        self.users.append(u2)
        self.posts.append(p1)

    def tearDown(self):
        for like in self.likes:
            db.session.delete(like)
        for post in self.posts:
            db.session.delete(post)
        for user in self.users:
            db.session.delete(user)

        db.session.commit()

    def test_post_model(self):
        """Does basic model work?"""

        p = Post(
            username="t1",
            title="gluttony",
            content="vice that creeps up on you"
        )

        db.session.add(p)
        db.session.commit()
        self.posts.append(p)

        # User should have no messages & no followers
        self.assertEqual(len(p.likes), 0)
        self.assertEqual(len(p.comments), 0)

    def test_likes(self):
        self.assertEqual(len(self.posts[0].likes), 0)
        l = Like(username="t2",post_id=self.posts[0].id,)

        db.session.add(l)
        db.session.commit()
        self.likes.append(l)

        self.assertEqual(len(self.posts[0].likes), 1)
        
    def test_comments(self):
        c = Comment(content="Jesus is the master", post_id=self.posts[0].id, username=self.users[1].username)

        db.session.add(c)
        db.session.commit()

        self.assertEqual(self.posts[0].comments[0].content, "Jesus is the master")
        self.assertEqual(len(self.posts[0].comments), 1)