from chathouse.rest.tokens.access.controller import GetAccessController
from flask_restful import Resource,request

class AccessResource(Resource):
	'''
	GrantResource - a class, meant to handle any post requests according to the endpoint /api/tokens/grant.

	Inherits: Resource.
	
	Methods:
		get - a method defined to handle get request aimed at the /api/tokens/grant.
	'''
	def get(self):
		'''
		Goal: control the handling of the post request.
		Purpose: return an access token based on the provided grant token.
		
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			GET -> GetAccessController.handle(headers,data) -> GetAccessStrategy.accept(headers,data,kwargs).
		
		Returns: response:tuple(JSON_Response:dict,status_code:int)
		'''
		return GetAccessController.handle(dict(request.headers),dict(request.data))