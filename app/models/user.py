from app import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.String(80), unique=True, nullable=False )
    name = db.Column(db.String(80), unique=True, nullable=False )
    password = db.Column(db.String(255), nullable=False )
    email = db.Column(db.String(120), unique=True, nullable=False)
    number = db.Column(db.String(16), nullable=False )
    date = db.Column(db.String(10), nullable=False )

    def __init__(self, name, nick_name, password, email, number, date):
        self.name = name
        self.nick_name = nick_name
        self.password = password
        self.email = email
        self.date = date
        self.number = number
    
    def __repr__(self):
        return "<User %r>" % self.email