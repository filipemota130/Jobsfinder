from app import db

class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False )
    category = db.Column(db.String(80), nullable=False )
    valor = db.Column(db.String(), nullable=False)
    desc = db.Column(db.String(), nullable=False )
    outros = db.Column(db.String(), nullable=False )
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    freelacer = db.relationship('User', foreign_keys = id_user)

    def __init__(self, name, category, valor, desc, outros, id_user):
        self.name = name
        self.category = category
        self.valor = valor
        self.desc = desc
        self.outros = outros
        self.id_user = id_user
    
    def __repr__(self):
        return "<Job %r>" % self.id