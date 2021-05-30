from flask_restful import Resource
from flask import request
from chathouse.rest.key_parameters.controller import GetKeyParametersController

class KeyParametersResource(Resource):
	'''
	KeyParametersResource - a class, meant to handle any requests according to the endpoint /api/key-parameters and the implemented methods.

	Inherits: Resource.
	
	Methods:
		get - a method defined to handle get requests aimed at the /api/key-parameters.
	'''

	def get(self):
		'''
		Goal: control the handling of the get request.
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			GET -> GetKeyParametersController.handle(headers,data) -> GetKeyParametersStrategy.accept(headers,data,kwargs).
		Kwargs:
			identification: requested identification as a part of the URI.
		Returns: response:tuple(JSON_Response:dict,status_code:int)
		'''

		return GetKeyParametersController.handle(dict(request.headers),{})