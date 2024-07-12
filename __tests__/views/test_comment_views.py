"""Comment views tests."""

# run these tests like:
#
#    python -m unittest __tests__/views/test_comment_views.py


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


class CommentViewsTestCase(TestCase):
    """Test views for comments."""

    def setUp(self):
        """Create test client, add sample data."""
        
        self.users = []
        self.posts = []
        self.comments = []
        
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

        c1 = Comment(
            content="serve the son as well",
            post_id=p1.id,
            username="t2"
            )

        db.session.add(c1)
        db.session.commit()

        self.comments.append(c1)
        self.posts.append(p1)
        self.users.append(u2)

    def tearDown(self):
        for comment in self.comments:
            db.session.delete(comment)
        for post in self.posts:
            db.session.delete(post)
        for user in self.users:
            db.session.delete(user)

        db.session.commit()

    def test_create_comment(self):
        """Create a comment"""

        # GET /forum/posts/<int:post_id>/comments
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 't1'

            resp = client.get(f'forum/posts/{self.posts[0].id}/comments')
            html = resp.get_data(as_text=True)

            self.assertIn('Make A Comment',html)

        # POST /forum/posts/<int:post_id>/comments
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 't1'

            resp = (client.post(f'forum/posts/{self.posts[0].id}/comments',
            data={'content':'serve the son as well'},follow_redirects=True))
            html = resp.get_data(as_text=True)

            self.assertIn('God the father',html)
            self.assertIn('Add Comment',html)

    def test_edit_comment(self):
        """Edit a comment"""

        # GET /forum/posts/<int:post_id>/comments/<int:comment_id>/edit
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 't2'

            resp = client.get(f'forum/posts/{self.posts[0].id}/comments/{self.comments[0].id}/edit')
            html = resp.get_data(as_text=True)

            self.assertIn('Edit A Comment',html)

        # POST /forum/posts/<int:post_id>/comments/<int:comment_id>/edit
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 't2'

            resp = (client.post(f'forum/posts/{self.posts[0].id}/comments/{self.comments[0].id}/edit',
            data={'content':'Ask for the holy spirit'},follow_redirects=True))
            html = resp.get_data(as_text=True)

            self.assertIn('Ask for the holy spirit',html)
            self.assertIn('Add Comment',html)

    def test_delete_comment(self):
        """Delete a comment"""

        # POST /forum/posts/<int:post_id>/comments/<int:comment_id>/delete
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 't2'

            self.assertEqual(len(Comment.query.all()),1)

            resp = client.post(f'/forum/posts/{self.posts[0].id}/comments/{self.comments[0].id}/delete',follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('Add Comment',html)
            self.assertEqual(len(Comment.query.all()),0)