"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template, flash, session,jsonify
from models import db, connect_db, User, Post, Comment, Player, LikeButton
from forms import RegisterForm, LoginForm, GameForm, SelectForm, PlayerForm, PostForm, CommentForm
# from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
import bcrypt

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Capstone_one_basketball'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Godalone1."
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)
db.drop_all()
db.create_all()

bcrypt = Bcrypt()

@app.route('/')
def homepage():
    if 'username' not in session:
        return render_template('home.html')
    return redirect(f"/{session['username']}/basketball-info")

@app.route('/<username>/basketball-info',methods=["GET","POST"])
def show_basketball_stuff(username):
    """ Landing page for login """
    if 'username' in session:
        if session['username'] == username:
            form = SelectForm()
            if form.validate_on_submit():
                info = form.info.data
                
                if info == "games":
                    return redirect(f"/{session['username']}/basketball-info/Game_Scores")
                if info == "player_stats_raw":
                    return redirect(f"/{session['username']}/basketball-info/player-stats-raw")
                if info == "player_stats_percentages":
                    return redirect(f"/{session['username']}/basketball-info/player-stats-percentages")
            return render_template('new_home.html',form=form,username=username)
        else:
            flash("You cannot access that page")
            flash("Did you mean this?")
            return redirect(f"/{session['username']}/basketball-info")

    flash("You must be logged in")
    return redirect('/login')

@app.route('/<username>/basketball-info/Game_Scores')
def show_games_stats(username):
    """ Page to check """
    if 'username' in session:
        if session['username'] == username:
            form = GameForm()
            return render_template('Game_Scores.html',form=form,username=username)
        else:
            flash("You cannot access that page")
            flash("Did you mean this?")
            return redirect(f"/{session['username']}/basketball-info/Game_Scores")
    
    flash("You must be logged in")
    return redirect('/login')

@app.route('/<username>/basketball-info/player-stats-raw')
def show_raw_player_stats(username):
    if 'username' in session:
        if session['username'] == username:
            print(session['username'])
            form = PlayerForm()
            return render_template('player_stats_raw.html',form=form,username=username)
        else:
            flash("You cannot access that page")
            flash("Did you mean this?")
            return redirect(f"/{session['username']}/basketball-info/player-stats-raw")
    
    flash("You must be logged in")
    return redirect('/login')

@app.route('/<username>/basketball-info/player-stats-percentages')
def show_percent_player_stats(username):
    if 'username' in session:
        if session['username'] == username:
            print(session['username'])
            form = PlayerForm()
            return render_template('player_stats_percentages.html',form=form,username=username)
        else:
            flash("You cannot access that page")
            flash("Did you mean this?")
            return redirect(f"/{session['username']}/basketball-info/player-stats-percentages")
    
    flash("You must be logged in")
    return redirect('/login')

@app.route('/<username>/basketball-info/charts')
def bar_chart(username):
    if 'username' in session:
        if session['username'] == username:
            return render_template('bar_chart.html',username=username)
        else:
            flash("You cannot access that page")
            flash("Did you mean this?")
            return redirect(f"/{session['username']}/basketball-info/charts")

    flash("You must be logged in")
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        favorite_player = form.favorite_player.data
        test_username = User.query.filter_by(username=username).first()
        if not test_username:
            password = form.password.data


            hashed = bcrypt.generate_password_hash(password)
            hashed_utf8 = hashed.decode("utf8")

            user = User(username=username, password=hashed_utf8,favorite_player=favorite_player)
            db.session.add(user)

            db.session.commit()

            session['username'] = username
            return redirect(f"/{session['username']}/basketball-info")
        else:
            flash("That username is already taken")
            return render_template('register.html',form=form)
    return render_template('register.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = username
            return redirect(f"/{session['username']}/basketball-info")

        flash("You need to enter proper credentials")
        return redirect('/login')
    return render_template('login.html',form=form)

@app.route('/logout',methods =["POST"])
def logout():
    session.pop('username')

    return redirect('/')

@app.route('/users')
def get_users():
    users = User.query.all()
    return render_template('users.html',users=users)

@app.route('/users/<username>')
def get_user(username):
    user = User.query.filter_by(username=username).first()
    return render_template("user_detail.html",user=user)

@app.route('/<username>/basketball-forum',methods= ["GET","POST"])
def forum(username):
    if 'username' in session:
        if session['username'] == username:
            posts = Post.query.all()
            return render_template('forum.html',posts=posts,username=username)
        else:
            flash("You cannot access that page")
            flash("Did you mean this?")
            return redirect(f"/{session['username']}/basketball-forum")
    flash("You must be logged in")
    return redirect('/login')


@app.route('/<username>/basketball-forum/<int:post_id>')
def post_detail(username,post_id):
    if 'username' in session:
        if session['username'] == username:
            session_username = session['username']

            post = Post.query.get(post_id)
            return render_template('post_detail.html',post=post,session_username=session_username,username=username)
        else:
            flash("You cannot access that page")
            flash("Did you mean this?")
            return redirect(f"/{session['username']}/basketball-forum/{post_id}")
    
    flash("You must be logged in")
    return redirect('/login')

@app.route('/<username>/basketball-forum/create-post', methods=["GET","POST"])
def create_post(username):
    if 'username' in session:
        if session['username'] == username:
            form = PostForm()
            if form.validate_on_submit():
                title = form.title.data
                content = form.content.data
                username = session['username']

                post = Post(title=title,content=content,username=username)

                db.session.add(post)
                db.session.commit()
                return redirect(f"/{session['username']}/basketball-forum")
            return render_template('post_form.html',form=form,username=username)
        else:
            flash("You cannot access that page")
            flash("Did you mean this?")
            return redirect(f"/{session['username']}/basketball-forum/create-post")
    flash("You must be logged in")
    return redirect('/login')

@app.route('/<username>/basketball-forum/<int:post_id>/delete-post', methods=["POST"])
def delete_post(username,post_id):
    if 'username' in session:
        if session['username'] == username:
            post = Post.query.get(post_id)
    
            db.session.delete(post)
            db.session.commit()

            return redirect(f"/{session['username']}/basketball-forum")
        else:
            flash("You cannot delete that")
            return redirect(f"/{session['username']}/basketball-forum/{post_id}")
    flash("You must be logged in")
    return redirect('/login')

@app.route('/<username>/basketball-forum/<int:post_id>/edit-post', methods =["GET","POST"])
def patch_post(username,post_id):
    if 'username' in session:
        if session['username'] == username:
            form = PostForm()
            if form.validate_on_submit():
                title = form.title.data
                content = form.content.data

                post.query.get(post_id)
                post.title = title
                post.content = content

                db.session.commit()

                return redirect(f"/{session['username']}/forum") 
            return render_template('edit_post_form.html',form=form,username=username)
        else:
            flash("You cannot access that page")
            return redirect(f"/{session['username']}/basketball-forum/{post_id}")
    flash("You must be logged in")
    return redirect('/login')

@app.route('/<username>/basketball-forum/<int:post_id>/create-comment', methods=["GET","POST"])
def create_comment(username,post_id):
    if 'username' in session:
        if session['username'] == username:
            form = CommentForm()
            if form.validate_on_submit():
                content = form.content.data

                comment = Comment(content=content, post_id=post_id)
                db.session.add(comment)

                db.session.commit()

                return redirect(f"/{session['username']}/basketball-forum/{post_id}")
            return render_template('comment_form.html',form=form,username=username)
        else:
            flash("You cannot access that page")
            return redirect(f"/{session['username']}/basketball-forum/{post_id}")
    flash("You must be logged in")
    return redirect('/login')

@app.route('/<username>/basketball-forum/<int:post_id>/<int:comment_id>/edit-comment', methods=["GET","POST"])
def edit_comment(username,post_id,comment_id):
    if 'username' in session:
        if session['username'] == username:
            form = CommentForm()
            if form.validate_on_submit():
                content = form.content.data

                comment = Comment.query.get(comment_id)
                comment.content = content

                db.session.commit()
                print("BYEEE")
                return redirect(f"/{session['username']}/basketball-forum/{post_id}")
            return render_template('edit_comment_form.html',form=form,username=username)
        else:
            flash("You cannot access that page")
            return redirect(f"/{session['username']}/basketball-forum/{post_id}")
    flash("You must be logged in")
    return redirect('/login')

@app.route('/<username>/basketball-forum/<int:post_id>/<int:comment_id>/delete-comment', methods=["POST"])
def delete_comment(username,post_id,comment_id):
    if 'username' in session:
        if session['username'] == username:
            comment = Comment.query.get(comment_id)
    
            db.session.delete(comment)
            db.session.commit()

            return redirect(f"/{session['username']}/basketball-forum/{post_id}")
        else:
            flash("You cannot delete that")
            return redirect(f"/{session['username']}/basketball-forum/{post_id}")
    flash("You must be logged in")
    return redirect('/login')

@app.route('/<username>/basketball-forum/<int:post_id>/like', methods=["POST"])
def like(username,post_id):
    if 'username' in session:
        post = Post.query.get(post_id)
        post_username = username
        like_username = session['username']
        clicked = request.args.get('clicked')
        check_button = LikeButton.query.filter((LikeButton.like_username==like_username) & (LikeButton.post_username==post_username) &
        (post_id==post_id)).first()

    
        if check_button == None:
            like_button = LikeButton(like_username=like_username,post_username=post_username,post_id=post_id,clicked=True)
            db.session.add(like_button)

            db.session.commit()
            print(like_button.clicked,"CLICKED CHECKER!!!!")
        else:
            if clicked == 'false':
                print(check_button.clicked,"CLICKED CHECKER!!!!")
                check_button.clicked = False

                db.session.commit()
            else:
                check_button.clicked = True

                db.session.commit()

        if clicked == 'true':
            post.likes += 1
        else:
            post.likes -= 1

        db.session.commit()

    return jsonify({"message":"Successful Click!"})

@app.route('/<username>/basketball-forum/<int:post_id>/like/state')
def get_like_state(username,post_id):
    post_username = username
    like_username = session['username']
    like_button = LikeButton.query.filter((LikeButton.like_username==like_username) & (LikeButton.post_username==post_username) &
    (post_id==post_id)).first()
    print("BYEEE")
    if like_button == None:
        print("HIIII3")
        return {"clicked":"false"}
    elif like_button:
        if like_button.clicked == True:
            print("HIIII1")
            return jsonify({"clicked":"true"})
        else:
            print("HIII2")
            return jsonify({"clicked":"false"})
    else:
        print("HIII4")
        return jsonify({"clicked":"false"})
