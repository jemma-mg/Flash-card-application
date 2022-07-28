from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

#Models for the Project
class User(db.Model,UserMixin):
    __tablename__='User'
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    username=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    fs_uniquifier=db.Column(db.String,unique=True,nullable=False)
    active=db.Column(db.Boolean)


#Decks table : contains info on Decks , connects to User by foreign key username
class Decks(db.Model):
    __tablename__='Decks'
    d_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    d_user=db.Column(db.Integer,db.ForeignKey('User.id'),nullable=False)
    d_name=db.Column(db.String,nullable=False)
    d_description=db.Column(db.String)

#Cards table: contains info on Cards , connects to User by foreign key username
class Cards(db.Model):
    __tablename__='Cards'
    c_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    c_deck=db.Column(db.Integer,db.ForeignKey('Decks.d_id'),nullable=False)
    c_user=db.Column(db.Integer,db.ForeignKey('User.id'),nullable=False)
    c_name=db.Column(db.String,nullable=False)
    c_description=db.Column(db.String,nullable=False)

class Review(db.Model):
    __tablename__='Review'
    r_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    r_user=db.Column(db.Integer,db.ForeignKey('User.id'),nullable=False)
    r_deck=db.Column(db.Integer,db.ForeignKey('Decks.d_id'),nullable=False)
    r_time=db.Column(db.String)
    r_score=db.Column(db.Float)
