import os

class Config:
	DEBUG=False
	TESTING=False
	SESSION_COOKIE_SECURE=True
	
	SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI','')

	MAIL_SERVER='smtp.gmail.com'
	MAIL_PORT=465
	MAIL_USE_SSL=True
	MAIL_USE_TLS=False
	MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
	MAIL_DEFAULT_SENDER=MAIL_USERNAME
	
	STATIC_KEY=os.environ.get('STATIC_KEY','')
	DH_PARAMETERS=int(os.environ.get('DH_GENERATOR',2)),int(os.environ.get('DH_MODULUS',11))

class DevelopmentConfig(Config):
	DEBUG=True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SESSION_COOKIE_SECURE=False

class TestingConfig(Config):
	TESTING=False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	DEBUG=True

class ProductionConfig(Config):
	pass