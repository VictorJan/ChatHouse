from chathouse.rest.tokens.verification.controller import PostVerificationController
from flask_restful import Resource,request

class VerificationResource(Resource):
	def post(self):
		return PostVerificationController.handle(dict(request.headers),request.json)