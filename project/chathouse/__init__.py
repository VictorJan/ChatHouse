import os
from flask import Flask



def create_app():
	app = Flask(__name__)
	try:
		app.config.from_object(f"config.{os.environ['ENVIRONMENT']}Config")
	except:
		app.config.from_object('config.Config')


	from chathouse.utilities.service.mail import mail
	mail.init_app(app)

	from chathouse.models import db
	db.init_app(app)
	create_db(app,db)

	from chathouse.migrations import migrate

	migrate.init_app(app,db)

	from chathouse.views import public,authorized
	#blueprints views
	app.register_blueprint(public)
	app.register_blueprint(authorized)

	#rest api resources
	from chathouse.rest import api
	api.init_app(app)
	
	from chathouse.socket import socket
	socket.init_app(app)
	#socket namespaces
	#socket.on_namespace(Namespace('/'))
	return app

def create_db(app,db):
	if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
		db.create_all(app=app)
	return None

