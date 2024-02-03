from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, DateField, TimeField
from wtforms.validators import Length

class RegisterForm(FlaskForm):

    username = StringField("Username", validators=[Length(min=5)])

    password = StringField("Password", validators=[Length(min=5)])

    favorite_player = StringField("Favorite Player")

class LoginForm(FlaskForm):

    username = StringField("Username", validators=[Length(min=5)])

    password = StringField("Password", validators=[Length(min=5)])

class GameForm(FlaskForm):

    date = DateField("Date", format='%Y-%m-%d')

    team1 = StringField("Team 1")

    team2 = StringField("Team 2")