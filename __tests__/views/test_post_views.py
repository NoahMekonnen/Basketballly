"""Post views tests."""

# run these tests like:
#
#    python -m unittest __tests/views/test_post_views.py


import os
from unittest import TestCase

from models import db, User, Like, Post, Comment
from flask_bcrypt import Bcrypt


from app import app

os.environ['DATABASE_URL'] = "postgresql://noah:Godalone1.@localhost:5432/Capstone_one_basketball_test"
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

bcrypt = Bcrypt()


# db.drop_all()
# db.create_all()


class PostViewsTestCase(TestCase):
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

        p1 = Post(
            title="God the father",
            content="serve him",
            username='t1'
        )

        db.session.add(p1)
        db.session.commit()

        self.posts.append(p1)
        self.users.append(u2)

    def tearDown(self):
        for post in self.posts:
            db.session.delete(post)
        for user in self.users:
            db.session.delete(user)

        db.session.commit()

    def test_forum(self):
        """Basketball Forum Page"""

        # GET /forum
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 't1'

            resp = client.get('/forum')
            html = resp.get_data(as_text=True)

            self.assertIn('Basketball Forum',html)

    def test_create_post(self):
        """Make a post"""

        # GET /forum/posts
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 't1'

            resp = client.get('forum/posts')
            html = resp.get_data(as_text=True)

            self.assertIn('Make A Post',html)

        # POST /forum/posts
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 't1'
            
            resp = client.post('forum/posts',data={'title':'Trinity', 'content':'serve perfectly'},follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('Basketball Forum',html)

    def test_post_detail(self):
        """View detail page of a post"""

        # GET /forum/posts/<int:post_id>
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 't1'

            resp = client.get(f'/forum/posts/{self.posts[0].id}')
            html = resp.get_data(as_text=True)

            self.assertIn('God the father',html)
            self.assertIn('serve him',html)
            self.assertIn('Add Comment',html)

    def test_patch_post(self):
        """Edit a post"""

        # GET /forum/posts/<int:post_id>/edit
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 't1'

            resp = client.get(f'/forum/posts/{self.posts[0].id}/edit')
            html = resp.get_data(as_text=True)

            self.assertIn('Title',html)
            self.assertIn('Content',html)

        # POST /forum/posts/<int:post_id>/edit
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 't1'

            resp = (client.post(f'/forum/posts/{self.posts[0].id}/edit',
            data={'title':'God the son', 'content':'think of him often'},follow_redirects=True))
            html = resp.get_data(as_text=True)

            self.assertIn('God the son',html)
            self.assertIn('Basketball Forum',html)

    def test_delete_post(self):
        """Delete a post"""

        # POST /forum/posts/<int:post_id>/delete
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 't1'

            resp = client.post(f'/forum/posts/{self.posts[0].id}/delete',follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('Basketball Forum',html)
            self.assertEqual(len(Post.query.all()),0)
