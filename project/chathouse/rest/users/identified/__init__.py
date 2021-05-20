'''
[Endpoint]Resource
This file shall contain defined Resource classes for this specific [Endpoint]=Users=/api/users:
[IdentifiedUser]Resource = /api/users/<identification>
'''
from chathouse.rest.users.identified.controller.get import GetIdentifiedUserController
from flask_restful import Resource,request

class IdentifiedUserResource(Resource):
	'''
	UsersResource - a class, meant to handle any get requests according to the endpoint /api/users.

	Inherits: Resource.
	
	Methods:
		get - a method defined to handle get requests aimed at the /api/users/<identification>.
	'''
	def get(self,identification):
		'''
		Goal: control the handling of the get request.
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			GET -> GetIdentifiedUserController.handle(headers,data) -> GetIdentifiedUserStrategy.accept(headers,data,kwargs).
		Kwargs:
			identification: requested identification as a part of the URI.
		Returns: response:tuple(JSON_Response:dict,status_code:int)
		'''
		return GetIdentifiedUserController.handle(dict(request.headers), data if (data:=request.json) else {} , identification=identification)