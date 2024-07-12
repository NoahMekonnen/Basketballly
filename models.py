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

    posts = db.relationship('Post', cascade = "all, delete-orphan", backref = 'user')

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.Text, db.ForeignKey('users.username', ondelete="cascade"), nullable = False)

    title = db.Column(db.Text, nullable = False)

    content = db.Column(db.Text, nullable = False)

    likes = db.relationship('Like', cascade="all, delete-orphan", backref='post')

    comments = db.relationship('Comment', cascade = "all, delete-orphan", passive_deletes=True, backref = 'post')


class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    content = db.Column(db.Text, nullable=False)   

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete="cascade"), nullable=False)

    username = db.Column(db.Text, db.ForeignKey('users.username', ondelete="cascade"), nullable=False)

class Like(db.Model):

    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete="cascade"), primary_key=True, nullable = False)

    username = db.Column(db.Text, db.ForeignKey('users.username', ondelete="cascade"), primary_key=True, nullable = False)

