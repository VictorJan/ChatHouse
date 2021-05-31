'''
This file shall contain initialization of each table in the database:
User;
Chat;
Message;
Participation;
Keyring.
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime
from time import time


metadata = MetaData( naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

db=SQLAlchemy(metadata=metadata)

class User(db.Model):
	__table_args__=(db.UniqueConstraint('username','email'),)

	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(30),nullable=False)
	email=db.Column(db.String,nullable=False)
	name=db.Column(db.String(25),nullable=False)
	password=db.Column(db.String(64),nullable=False)
	about=db.Column(db.String,nullable=False)
	activity_dnt=db.Column(db.DateTime,default=lambda:datetime.fromtimestamp(int(time())))

	keyring=db.relationship('Keyring',backref='owner',cascade='all,delete',lazy=True,uselist=False)
	participations=db.relationship('Participation',backref='participant',cascade='all,delete', lazy='dynamic')
	creations=db.relationship('Chat',backref='creator',cascade='all,delete', lazy='dynamic')
	messages=db.relationship('Message',backref='sender',cascade='all,delete',lazy='dynamic')

class Chat(db.Model):

	id=db.Column(db.Integer,primary_key=True)
	creator_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
	name=db.Column(db.String,nullable=False)
	creation_dnt=db.Column(db.DateTime,default=lambda:datetime.fromtimestamp(int(time())))
	activity_dnt=db.Column(db.DateTime,default=lambda:datetime.fromtimestamp(int(time())))

	messages=db.relationship('Message',backref='chat',cascade='all,delete',lazy='dynamic')
	participations=db.relationship('Participation',backref='chat',cascade='all,delete',lazy='dynamic')


class Message(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	sender_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
	chat_id=db.Column(db.Integer,db.ForeignKey('chat.id'),nullable=False)
	content=db.Column(db.PickleType,nullable=False)
	dnt=db.Column(db.DateTime,default=lambda:datetime.fromtimestamp(int(time())))

class Participation(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	participant_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
	chat_id=db.Column(db.Integer,db.ForeignKey('chat.id'),nullable=False)

class Keyring(db.Model):
	__table_args__=(db.UniqueConstraint('owner_id','public_key','private_key'),)

	id=db.Column(db.Integer,primary_key=True)
	owner_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
	public_key=db.Column(db.Integer,nullable=False)
	private_key=db.Column(db.PickleType,nullable=False)
	dnt=db.Column(db.DateTime,default=lambda:datetime.fromtimestamp(int(time())))





