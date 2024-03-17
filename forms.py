from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, DateField, TimeField, SelectField
from wtforms.validators import Length

class RegisterForm(FlaskForm):

    username = StringField("Username", validators=[Length(min=5)])

    password = PasswordField("Password", validators=[Length(min=5)])

    favorite_player = StringField("Favorite Player")

class LoginForm(FlaskForm):

    username = StringField("Username", validators=[Length(min=5)])

    password = PasswordField("Password", validators=[Length(min=5)])

class GameForm(FlaskForm):

    date = DateField("Date", format='%Y-%m-%d')

    team1 = StringField("Team 1")

    team2 = StringField("Team 2")

class PostForm(FlaskForm):

    title = StringField("Title")

    content = StringField("Content")

class CommentForm(FlaskForm):

    content = StringField("Content")

class SelectForm(FlaskForm):

    info = SelectField("What do you want to know?", choices=[("games","Games Scores"), ("player_stats_raw","Player Statistics(Raw stats)"),
    ("player_stats_percentages","Player Statistics(percentages)")])

class PlayerForm(FlaskForm):

    name = StringField("Name")

    team = StringField("Team")

    season = StringField("Season")


