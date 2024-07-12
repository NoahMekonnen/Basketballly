"""Chart views tests."""

# run these tests like:
#
#    python -m unittest __tests/views/test_chart_views.py


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


class ChartViewsTestCase(TestCase):
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

    def test_show_game_stats(self):
        """Show form for displaying game stats"""

        # GET /basketball-info/Game_Scores
        with app.test_client() as client:
            with client.session_transaction() as session:
               session['username'] = 't1'

            resp = client.get('basketball-info/Game_Scores')
            html = resp.get_data(as_text=True) 

            self.assertIn('Team 1',html)

    def test_show_raw_player_stats(self):
        """Show form for displaying raw player stats"""

        # GET /basketball-info/player-stats-raw
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 't1'
            
            resp = client.get('basketball-info/player-stats-raw')
            html = resp.get_data(as_text=True)

            self.assertIn('Player Stats(Raw)',html)
            self.assertIn('Season',html)

    def test_show_percent_player_stats(self):
        """Show form for displaying player stats in percentages/ratios"""

        # GET /basketball-info/player-stats-percentages
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 't1'
                
            resp = client.get('basketball-info/player-stats-percentages')
            html = resp.get_data(as_text=True)

            self.assertIn('Player Stats(Percent/Ratio)',html)
            self.assertIn('Season',html)