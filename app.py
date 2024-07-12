"""Flask app for Cupcakes"""
import os 

from flask import Flask, request, redirect, render_template, flash, session, jsonify
from models import db, connect_db, User, Post, Comment, Like
from forms import RegisterForm, LoginForm, GameForm, SelectForm, PlayerForm, PostForm, CommentForm
# from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
import bcrypt

app = Flask(__name__)
app.app_context().push()
# iagptsui:b0JCJsLrFruyu_EarcfGuxNdH5Bdlf6V@kala.db.elephantsql.com/iagptsui
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql://iagptsui:b0JCJsLrFruyu_EarcfGuxNdH5Bdlf6V@kala.db.elephantsql.com/iagptsui'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Godalone1."
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)
# db.drop_all()
# db.create_all()

bcrypt = Bcrypt()


@app.route('/')
def homepage():
    if 'username' in session:
        return redirect("/basketball-info")
    return redirect("/login")


@app.route('/basketball-info',methods=["GET","POST"])
def show_basketball_stuff():
    """ Landing page for login """

    form = SelectForm()
    if form.validate_on_submit():
        info = form.info.data
        if info == "games":
            return redirect("/basketball-info/Game_Scores")
        if info == "player_stats_raw":
            return redirect("/basketball-info/player-stats-raw")
        if info == "player_stats_percentages":
            return redirect("/basketball-info/player-stats-percentages")
    return render_template('new_home.html',form=form,username=session['username'])

################################################################ User Routes

@app.route('/register', methods=['GET','POST'])
def register(): 
    """ Register a user """

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        favorite_player = form.favorite_player.data
        existing_user = User.query.filter_by(username=username).first()
        
        if not existing_user:
            password = form.password.data

            hashed = bcrypt.generate_password_hash(password)
            hashed_utf8 = hashed.decode("utf8")

            user = User(username=username, password=hashed_utf8,favorite_player=favorite_player)
            db.session.add(user)

            db.session.commit()
        
            session['username'] = user.username
            return redirect("/basketball-info")
        else:
            flash("That username is already taken", "danger")
            return render_template('register.html',form=form)
    return render_template('register.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    """ Login """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            if bcrypt.check_password_hash(existing_user.password, password):
                session['username'] = existing_user.username
                return redirect("/basketball-info")
            else:
                flash("Invalid username/password", "danger")
        else:
            flash("A user with that username doesn't exist", "danger")

    return render_template('login.html',form=form)

@app.route('/users')
def get_users():
    """ Get all users """

    users = User.query.all()
    return render_template('users.html',users=users)

@app.route('/users/<username>')
def get_user(username):
    """ Get a user """

    user = User.query.filter_by(username=username).first()
    return render_template("user_detail.html",user=user)
    
################################################################ Chart Routes

@app.route('/basketball-info/Game_Scores')
def show_game_stats():
    """ Show Game Scores """

    form = GameForm()
    return render_template('Game_Scores.html',form=form)

@app.route('/basketball-info/player-stats-raw')
def show_raw_player_stats():
    """ Show raw player stats """

    form = PlayerForm()
    return render_template('player_stats_raw.html',form=form)

@app.route('/basketball-info/player-stats-percentages')
def show_percent_player_stats():
    """ Show player stats in percentages"""
            
    form = PlayerForm()
    return render_template('player_stats_percentages.html',form=form)

################################################################ Post Routes

@app.route('/forum')
def forum():
    if 'username' in session:
        posts = Post.query.all()
        return render_template('forum.html',posts=posts)
    return redirect('/login')

@app.route('/forum/posts', methods=["GET","POST"])
def create_post():
    """ Create a post """

    if 'username' in session:
        form = PostForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            username = session['username']

            post = Post(title=title,content=content,username=session['username'])

            db.session.add(post)
            db.session.commit()
            return redirect("/forum")
        return render_template('post_form.html',form=form)
    
    return redirect('/login')

@app.route('/forum/posts/<int:post_id>')
def post_detail(post_id):
    """ Get a post """
    
    if 'username' in session:
        post = Post.query.get(post_id)
        session_user = User.query.get(session['username'])
        post_user = User.query.get(post.username)
        is_owner = session_user == post_user
        return render_template('post_detail.html',post=post,is_owner=is_owner,session_username=session['username'],likes=post.likes)
    else:
        flash("You must be logged in","danger")
        return redirect('/login')

@app.route('/forum/posts/<int:post_id>/edit', methods =["GET","POST"])
def patch_post(post_id):
    """ Edit a post """

    if 'username' in session:
        post = Post.query.get(post_id)
        if session['username'] == post.username:
            form = PostForm()
            if form.validate_on_submit():
                title = form.title.data
                content = form.content.data

                post.title = title
                post.content = content

                db.session.commit()

                return redirect("/forum") 
            return render_template('edit_post_form.html',form=form,username=post.username)
        else:
            flash("You cannot access that page", "danger")
            return redirect(f"/{session['username']}/basketball-forum/{post_id}")
    flash("You must be logged in", "danger")
    return redirect('/login')

@app.route('/forum/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """ Delete a post """

    if 'username' in session:
        post = Post.query.get(post_id)
        if session['username'] == post.username:
    
            db.session.delete(post)
            db.session.commit()

            return redirect("/forum")
        flash("You can't delete someone else's post", "danger")
    else:
        flash("You must be logged in", "danger")
    return redirect('/login')

################################################################ Comment Routes

@app.route('/forum/posts/<int:post_id>/comments', methods=["GET","POST"])
def create_comment(post_id):
    """Create a comment"""
    if 'username' in session:
        form = CommentForm()
        if form.validate_on_submit():
            content = form.content.data

            comment = Comment(content=content, post_id=post_id, username=session['username'])
            db.session.add(comment)

            db.session.commit()

            return redirect(f"/forum/posts/{post_id}")
        return render_template('comment_form.html',form=form)
    flash("You must be logged in", "danger")
    return redirect('/login')

@app.route('/forum/posts/<int:post_id>/comments/<int:comment_id>/edit', methods=["GET","POST"])
def edit_comment(post_id,comment_id):
    """ Edit a comment """
    if 'username' in session:
        form = CommentForm()
        if form.validate_on_submit():
            content = form.content.data

            comment = Comment.query.get(comment_id)
            comment.content = content

            db.session.commit()

            return redirect(f"/forum/posts/{post_id}")
        return render_template('edit_comment_form.html',form=form,username=session['username'],post_id=post_id)
   
    flash("You must be logged in", "danger")
    return redirect('/login')

@app.route('/forum/posts/<int:post_id>/comments/<int:comment_id>/delete', methods=["POST"])
def delete_comment(post_id,comment_id):
    """Delete a comment"""
    if 'username' in session:
        comment = Comment.query.get(comment_id)
    
        db.session.delete(comment)
        db.session.commit()

        return redirect(f"/forum/posts/{post_id}")
    
    flash("You must be logged in", "danger")
    return redirect('/login')

################################################################ Like Routes

# In progress maybe
# @app.route('/forum/posts/<int:post_id>/like', methods=["POST"])
# def like_post(post_id):
#     """Like or unlike a post"""
#     if 'username' in session:
#         post = Post.query.filter_by(post_id=post_id).first()
#         like = Like.query.filter((Like.post_id == post_id) & (Like.username == session['username'])).first()
#         if not (post.username == session['username']) and not like:
#             new_like = Like(post_id=post_id, username=session['username'])

#             db.session.add(new_like)
#             db.session.commit()
#         elif like:
#             db.session.delete(like)
#             db.session.commit()

#     return jsonify({msg: "Unauthorized"})
    
@app.route('/login-state')
def change_login_status():
    if 'username' in session:
        return jsonify({"logged-in":True})
    return jsonify({"logged-in":False})

@app.route('/logout')
def logout_page():
    if 'username' in session:
        session.pop('username')
        flash("You have successfully logged out", "success")
    else:
        flash('You must be logged in to do that', "danger")
    return redirect('/login')

@app.route('/username')
def get_username():
    return jsonify({"username":session['username']})
