from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")

class CadastroForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    nickname = StringField("nickname", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    contact = IntegerField("contact", validators=[DataRequired()])
    birth_date = StringField("birth_date", validators=[DataRequired()])
    adress = StringField("adress", validators=[DataRequired()])
    compAdress = StringField("compAdress", validators=[DataRequired()])
    state = StringField("state", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])