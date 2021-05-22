'''
[Endpoint]Resource
This file shall contain defined Resource classes for this specific [Endpoint]=Users=/api/users/<identification>/participations:
[IdentifiedUserParticipantions]Resource = /api/users/<identification>/participations
'''
from chathouse.rest.users.identified.participations.controller import GetIdentifiedUserParticipationsController
from flask_restful import Resource,request

class IdentifiedUserParticipationsResource(Resource):
	'''
	IdentifiedUserParticipantionsResource - a class, meant to handle any get requests according to the endpoint /api/users/<identification>/participations.

	Inherits: Resource.
	
	Methods:
		get - a method defined to handle get requests aimed at the /api/users/<identification>/participations.
	'''
	def get(self,identification):
		'''
		Goal: control the handling of the get request.
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			GET -> GetIdentifiedUserParticipationsController.handle(headers,data) -> GetIdentifiedUserParticipantionsStrategy.accept(headers,data,kwargs).
		Kwargs:
			identification: requested identification as a part of the URI.
		Returns: response:tuple(JSON_Response:dict,status_code:int)
		'''
		return GetIdentifiedUserParticipationsController.handle(dict(request.headers), data if (data:=request.json) else {} , identification=identification)