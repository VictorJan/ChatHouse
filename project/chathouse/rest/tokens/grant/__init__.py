from chathouse.rest.tokens.grant.controller import PostGrantController
from flask_restful import Resource,request

class GrantResource(Resource):
	'''
	GrantResource - a class, meant to handle any post requests according to the endpoint /api/tokens/grant.

	Inherits: Resource.
	
	Methods:
		post - a method defined to handle post requests aimed at the /api/tokens/grant.
	'''
	def post(self):
		'''
		Goal: control the handling of the post request.
		
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			POST -> PostGrantController.handle(headers,data) -> PostGrantStrategy.accept(headers,data,kwargs).
		
		Returns: response:tuple(JSON_Response:dict,status_code:int)
		'''
		return PostGrantController.handle(dict(request.headers),data if (data:=request.json) else {} )