import json

with open('config.json') as config_file:
	config=json.load(config_file)

class Config:
	DEBUG=False
	TESTING=False
	SESSION_COOKIE_SECURE=True
	
	SQLALCHEMY_DATABASE_URI=config.get('SQLALCHEMY_DATABASE_URI','')

	MAIL_SERVER='smtp.gmail.com'
	MAIL_PORT=465
	MAIL_USE_SSL=True
	MAIL_USE_TLS=False
	MAIL_USERNAME=config.get('MAIL_USERNAME')
	MAIL_PASSWORD=config.get('MAIL_PASSWORD')
	MAIL_DEFAULT_SENDER=MAIL_USERNAME
	
	STATIC_KEY=config.get('STATIC_KEY','')
	DH_PARAMETERS=int(config.get('DH_GENERATOR',2)),int(config.get('DH_MODULUS',11))

	PREACCESS_EXP={'minutes':30}
	VERIFICATION_EXP={'minutes':2}
	GRANT_EXP={'minutes':30}
	ACCESS_EXP={'minutes':10}
	CONFIRMATION_EXP={'minutes':3}

class DevelopmentConfig(Config):
	DEBUG=True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SESSION_COOKIE_SECURE=False

class TestingConfig(Config):
	TESTING=True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	DEBUG=True

class ProductionConfig(Config):
	pass