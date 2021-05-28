'''
[Endpoint]Resource
This file shall contain defined Resource classes for this specific [IdentifiedUserKeyring]=Keyring=/api/users/<identification>/keyring:
[IdentifiedUserKeyring]Resource = /api/users/<identification>/keyring
'''
from chathouse.rest.users.identified.keyring.controller import GetIdentifiedUserKeyringController
from flask_restful import Resource,request

class IdentifiedUserKeyringResource(Resource):
	'''
	IdentifiedUserKeyringResource - a class, meant to handle any get requests according to the protected endpoint /api/users/<identification>/keyring.

	Inherits: Resource.
	
	Methods:
		get - a method defined to handle get requests aimed at the /api/users/<identification>/keyring.
	'''
	def get(self,identification):
		'''
		Goal: control the handling of the get request.
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			GET -> GetIdentifiedUserKeyringController.handle(headers,data) -> GetIdentifiedUserKeyringStrategy.accept(headers,data,kwargs).
		Kwargs:
			identification: requested identification as a part of the URI.
		Returns: response:tuple(JSON_Response:dict,status_code:int)
		'''
		return GetIdentifiedUserKeyringController.handle(dict(request.headers), data if (data:=request.json) else {} , identification=identification)