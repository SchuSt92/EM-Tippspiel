from db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Mannschaft(db.Model):
    __tablename__ = "mannschaft"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    abkuerzung = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    logo = db.Column(db.String(100), nullable=False)
    em_titel = db.Column(db.Integer, default=0)

class Spiel(db.Model):
    __tablename__ = "spiel"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Neue eindeutige ID als Primärschlüssel
    heim_mannschaft_id = db.Column(db.Integer, db.ForeignKey('mannschaft.id'))
    gast_mannschaft_id = db.Column(db.Integer, db.ForeignKey('mannschaft.id'))
    typ = db.Column(db.String(50))  # z.B. "Vorrunde", "Halbfinale", etc.
    tore_heim = db.Column(db.Integer, nullable=False, default=0)
    tore_gast = db.Column(db.Integer, nullable=False, default=0)
    austragungsort = db.Column(db.String(100), nullable=False)
    datum = db.Column(db.DateTime, nullable=False)
    gruppe = db.Column(db.String(1), nullable=True)
    absolviert = db.Column(db.Boolean, default=False, nullable=False)
    locked = db.Column(db.Boolean, default=False, nullable=False)
    heim_mannschaft = db.relationship("Mannschaft", foreign_keys=[heim_mannschaft_id])
    gast_mannschaft = db.relationship("Mannschaft", foreign_keys=[gast_mannschaft_id])


class Tipp(db.Model):
    __tablename__ = "tipp"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Neue eindeutige ID als Primärschlüssel
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    spiel_id = db.Column(db.Integer, db.ForeignKey('spiel.id'))
    tipp_tore_heim = db.Column(db.Integer, nullable=True, default=0)
    tipp_tore_gast = db.Column(db.Integer, nullable=True, default=0)
    punkte = db.Column(db.Integer, nullable=False, default=0)
    active = db.Column(db.Boolean, default=False, nullable=False)
    spiel = db.relationship("Spiel")
    user = db.relationship("User")


class Rangliste(db.Model):
    __tablename__ = "rangliste"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Neue eindeutige ID als Primärschlüssel
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    punkte = db.Column(db.Integer, nullable=False, default=0)
    user = db.relationship("User")