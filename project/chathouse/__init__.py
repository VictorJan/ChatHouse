import os
from flask import Flask



def create_app(config=None):
	'''
	Goal: creates an application, based on the requested config, following the factory pattern.
	Arguments: config:None|str.
	Actions:
		Intializes all of the required services: Mail,DataBase,Migrations,Blueprint Views,REST API Resources, Socket Namespaces.
	Returns: app.
	'''
	app = Flask(__name__)
	try:
		app.config.from_object(f"config.{os.environ['ENVIRONMENT'] if config is None else config}Config")
	except:
		app.config.from_object('config.Config')


	from chathouse.utilities.service.mail import mail
	mail.init_app(app)

	from chathouse.models import db
	db.init_app(app)
	create_db(app,db)

	from chathouse.migrations import migrate

	migrate.init_app(app,db,render_as_batch=True)

	from chathouse.views import public,authorized
	#blueprints views
	app.register_blueprint(public)
	app.register_blueprint(authorized)

	#rest api resources
	from chathouse.rest import api
	api.init_app(app)
	
	#socket namespaces
	from chathouse.socket import socket
	socket.init_app(app)
	return app

def create_db(app,db):
	'''
	Goal: create a database, if one doesn't already exist.
	Arguments:app,db.
	Returns:None
	'''
	if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
		db.create_all(app=app)
	return None

