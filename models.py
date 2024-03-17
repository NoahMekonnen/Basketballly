from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    username = db.Column(db.Text, primary_key=True)

    password = db.Column(db.Text)

    favorite_player = db.Column(db.Text)

    posts = db.relationship('Post', cascade = "all, delete", passive_deletes=True, backref = 'user')

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.Text, db.ForeignKey('users.username'), nullable = False)

    title = db.Column(db.Text, nullable = False)

    content = db.Column(db.Text, nullable = False)

    likes = db.Column(db.Integer, nullable = False, default=0)

    comments = db.relationship('Comment', cascade = "all, delete", passive_deletes=True, backref = 'post')


class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    content = db.Column(db.Text, nullable=False)   

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

class Game(db.Model):

    __tablename__ = "games"

    date = db.Column(db.Text, primary_key=True)

    team1 = db.Column(db.Text, primary_key=True)

    team2 = db.Column(db.Text, primary_key=True)

class Player(db.Model):

    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, nullable=False)

    free_throw_avg = db.Column(db.Float)

class LikeButton(db.Model):

    __tablename__ = "likebutton"

    like_username = db.Column(db.Text, db.ForeignKey('users.username'), primary_key=True, nullable = False)

    post_username = db.Column(db.Text, db.ForeignKey('users.username'), primary_key=True, nullable = False)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, nullable = False)

    clicked = db.Column(db.Boolean, nullable=False, default=False)