'''
[Endpoint]Resource
This file shall contain defined Resource classes for this specific [Endpoint]=Users=/api/users/<identification>:

[IdentifiedUser]Resource = /api/users/<identification>
[IdentifiedUserParticipations]Resource = /api/users/<identification>/participations
'''
from chathouse.rest.users.identified.controller import GetIdentifiedUserController,PutIdentifiedUserController,DeleteIdentifiedUserController
from flask_restful import Resource,request

from chathouse.rest.users.identified.participations import IdentifiedUserParticipationsResource
from chathouse.rest.users.identified.keyring import IdentifiedUserKeyringResource

class IdentifiedUserResource(Resource):
	'''
	IdentifiedUserResource - a class, meant to handle any get requests according to the endpoint /api/users/<identified>.

	Inherits: Resource.
	
	Methods:
		get - a method defined to handle get requests aimed at the /api/users/<identification>.
		put - a method defined to handle put requests aimed at the /api/users/<identification>.
		delete - a method defined to handle delete requests aimed at the /api/users/<identification>.
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
		return GetIdentifiedUserController.handle(dict(request.headers), {} , identification=identification)

	def put(self,identification):
		'''
		Goal: control the handling of the put request.
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			PUT -> PutIdentifiedUserController.handle(headers,data) -> PutIdentifiedUserStrategy.accept(headers,data,kwargs).
		Kwargs:
			identification: requested identification as a part of the URI.
		Returns: response:tuple(JSON_Response:dict,status_code:int)
		'''
		return PutIdentifiedUserController.handle(dict(request.headers), data if (data:=request.json) else {} , identification=identification)

	def delete(self,identification):
		'''
		Goal: control the handling of the put request.
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			DELETE -> DeleteIdentifiedUserController.handle(headers,data) -> DeleteIdentifiedUserStrategy.accept(headers,data,kwargs).
		Kwargs:
			identification: requested identification as a part of the URI.
		Returns: response:tuple(JSON_Response:dict,status_code:int)
		'''
		return DeleteIdentifiedUserController.handle(dict(request.headers), data if (data:=request.json) else {} , identification=identification)

