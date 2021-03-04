from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")


class CadastroForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    nick_name = StringField("nick_name", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    contact = IntegerField("contact", validators=[DataRequired()])
    birth_date = StringField("birth_date", validators=[DataRequired()])
    desc = TextAreaField("description")
