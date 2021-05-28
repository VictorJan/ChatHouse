from chathouse.rest.tokens.confirmation.controller import PostConfirmationController
from flask_restful import Resource,request

class ConfirmationResource(Resource):
	'''
	ConfirmationResource - a class, meant to handle any post requests according to the endpoint /api/tokens/confirmation.

	Inherits: Resource.
	
	Methods:
		post - a method defined to handle post requests aimed at the /api/tokens/confirmation.
	'''
	def post(self):
		'''
		Goal: control the handling of the post request.
		
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			POST -> PostConfirmationController.handle(headers,data) -> PostConfirmationStrategy.accept(headers,data,kwargs).
		
		Returns: response:tuple(JSON_Response:dict,status_code:int)
		'''
		return PostConfirmationController.handle(dict(request.headers), data if (data:=request.json) else {} )