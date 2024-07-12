"""User views tests."""

# run these tests like:
#
#    python -m unittest __tests/views/test_user_views.py


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


class UserViewsTestCase(TestCase):
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

    def test_register(self):
        """Register"""

        # GET /register
        with app.test_client() as client:
            resp = client.get('/register')
            html = resp.get_data(as_text=True)

            self.assertIn('Register',html)
            self.assertIn('Favorite Player',html)

        # POST /register
        with app.test_client() as client:
            resp = client.post('/register',data={'username':'test1','password':'HASHED_PASSWORD'},follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('Baller Chatroom',html)

        user = User.query.get('test1')
        self.users.append(user)

    def test_login(self):
        """Login"""

        # GET /login
        with app.test_client() as client:
            resp = client.get('/login')
            html = resp.get_data(as_text=True)

            self.assertIn('Login',html)
            self.assertIn('Username',html)
            self.assertNotIn('Favorite Player',html)

        # POST /login
        with app.test_client() as client:
            client.post('/register',data={'username':'test1','password':'HASHED_PASSWORD'},follow_redirects=True)
            resp = client.post('/login',data={'username':'test1','password':'HASHED_PASSWORD'},follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('Baller Chatroom',html)

        user = User.query.get('test1')
        self.users.append(user)

    def test_get_users(self):
        """Getting all users"""

        # GET /users
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertIn('t1',html)

    def test_get_user(self):
        """Get a user"""

        # GET /users/<username>
        with app.test_client() as client:
            resp = client.get(f'/users/{self.users[0].username}')  
            html = resp.get_data(as_text=True)

            self.assertIn('No Posts...',html)

    
