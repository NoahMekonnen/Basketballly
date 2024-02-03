"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template, flash, session,jsonify
from models import db, connect_db, User
from forms import RegisterForm, LoginForm, GameForm
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
import bcrypt

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Godalone1."
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.drop_all()
db.create_all()

bcrypt = Bcrypt()

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/basketball-info',methods=["GET","POST"])
def show_basketball_stuff():
    form = GameForm()
    if 'username' in session:
        return render_template('new_home.html',form=form)

    flash("You must be logged in")
    return redirect('/login')

@app.route('/basketball-info/charts')
def bar_chart():
    if 'username' in session:
        return render_template('bar_chart.html')

    flash("You must be logged in")
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        user = User(username=username, password=hashed_utf8)
        db.session.add(user)

        db.session.commit()

        session['username'] = username
        return redirect('/basketball-info')
    return render_template('register.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=sername).first()
        if user and bcrypt.check_password_hash(u.password, pwd):
            session['username'] = username
            return redirect('/basketball-info')

        flash("You need to enter proper credentials")
        return render_template('/login')
    return render_template('login.html',form=form)
