from flask_sqlalchemy import SQLAlchemy
import datetime,time

db=SQLAlchemy()

class User(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(30),unique=True,nullable=False)
	email=db.Column(db.String(40),unique=True,nullable=False)
	name=db.Column(db.String(25),nullable=False)
	password=db.Column(db.String(64),nullable=False)

	keyring=db.relationship('Keyring',backref='owner',cascade='all,delete',lazy=True,uselist=False)
	participations=db.relationship('Participation',backref='participant',cascade='all,delete', lazy=True)
	messages=db.relationship('Message',backref='sender',cascade='all,delete',lazy=True)

class Chat(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	dnt=db.Column(db.DateTime,default=datetime.datetime.fromtimestamp(int(time.time())))

	messages=db.relationship('Message',backref='chat',cascade='all,delete',lazy=True)
	participations=db.relationship('Participation',backref='chat',cascade='all,delete',lazy=True)


class Message(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	sender_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
	chat_id=db.Column(db.Integer,db.ForeignKey('chat.id'),nullable=False)
	content=db.Column(db.Text,nullable=False)
	dnt=db.Column(db.DateTime,default=datetime.datetime.fromtimestamp(int(time.time())))

class Participation(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	participant_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
	chat_id=db.Column(db.Integer,db.ForeignKey('chat.id'),nullable=False)

class Keyring(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	owner_id=db.Column(db.Integer,db.ForeignKey('user.id'),unique=True,nullable=False)
	public_key=db.Column(db.Integer,nullable=False)
	private_key=db.Column(db.Text,unique=True,nullable=False)
	dnt=db.Column(db.DateTime,default=datetime.datetime.fromtimestamp(int(time.time())))





