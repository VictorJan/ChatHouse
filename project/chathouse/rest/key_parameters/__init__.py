from flask_restful import Resource
from flask import request
from chathouse.rest.key_parameters.controller import GetKeyParametersController

class KeyParametersResource(Resource):
	def get(self):
		return GetKeyParametersController.handle(dict(request.headers),request.data)