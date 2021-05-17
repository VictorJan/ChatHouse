from chathouse.rest.tokens.verification.controller import PostVerificationController
from flask_restful import Resource,request

class VerificationResource(Resource):
	'''
	VerificationResource - a class, meant to handle any post requests according to the endpoint /api/tokens/verification.

	Inherits: Resource.
	
	Methods:
		post - a method defined to handle post requests aimed at the /api/tokens/verification.
	'''
	def post(self):
		'''
		Goal: control the handling of the post request.
		
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			POST -> PostVerificationController.handle(headers,data) -> PostVerificationStrategy.accept(headers,data,kwargs).
		
		Returns: response:tuple(JSON_Response:dict,status_code:int)
		'''
		return PostVerificationController.handle(dict(request.headers), data if (data:=request.json) else {} )