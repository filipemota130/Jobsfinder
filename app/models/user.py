from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.String(80), unique=True, nullable=False )
    name = db.Column(db.String(80), unique=True, nullable=False )
    password = db.Column(db.String(255), nullable=False )
    email = db.Column(db.String(120), unique=True, nullable=False)
    number = db.Column(db.String(16), nullable=False )
    date = db.Column(db.String(10), nullable=False )
    desc = db.Column(db.String())

    def set_senha(self, senha):
        self.password = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.password, senha)

    def __init__(self, name, nick_name, email, number, date, desc):
        self.name = name
        self.nick_name = nick_name
        self.email = email
        self.date = date
        self.number = number
        self.desc = desc
    
    def __repr__(self):
        return "<User %r>" % self.email