from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    username = db.Column(db.Text, primary_key=True)

    password = db.Column(db.Text)

    favorite_player = db.Column(db.Text)
    
class Game(db.Model):

    date = db.Column(db.Text, primary_key=True)

    team1 = db.Column(db.Text, primary_key=True)

    team2 = db.Column(db.Text, primary_key=True)
