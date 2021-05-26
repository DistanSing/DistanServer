"""
Schema for tables in the database.
Ruben Arellano
github.com/rarellano00
University of Utah
"""
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    fname = db.Column(db.String(75))
    lname = db.Column(db.String(75))
    publicip = db.Column(db.Integer)
    privateip = db.Column(db.Integer)
    port = db.Column(db.Integer)
    customidentifier = db.Column(db.String(15))
    # one to many relationship: a user can be in one rehearsal
    rehearsal_id = db.Column(db.Integer, db.ForeignKey('rehearsal.id'))


class Rehearsal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    hostname = db.Column(db.String(150))
    password = db.Column(db.String(100))
    active = db.Column(db.Boolean)
    # a rehearsal can have many users
    users = db.relationship("User", lazy='joined', cascade='all, delete-orphan')
