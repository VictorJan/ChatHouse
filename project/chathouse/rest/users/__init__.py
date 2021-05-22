'''
[Endpoint]Resource
This file shall contain defined Resource classes for this specific [Endpoint]=Users=/api/users/<identification>:
[Users]Resource = /api/users
[IdentifiedUser]Resource = /api/users/<identification>
'''
from chathouse.rest.users.controller.get import GetUsersController
from flask_restful import Resource,request


from chathouse.rest.users.identified import IdentifiedUserResource,IdentifiedUserParticipationsResource

class UsersResource(Resource):
	'''
	UsersResource - a class, meant to handle any get requests according to the endpoint /api/users.

	Inherits: Resource.
	
	Methods:
		get - a method defined to handle get requests aimed at the /api/users.
	'''
	def get(self):
		'''
		Goal: control the handling of the get request.
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			GET -> GetUsersController.handle(headers,data) -> GetUsersStrategy.accept(headers,data,kwargs).
		Kwargs:
			identification: requested identification as a GET parameter.
		Returns: response:tuple(JSON_Response:dict,status_code:int)
		'''
		return GetUsersController.handle(dict(request.headers), data if (data:=request.json) else {} , identification=request.args.get('identification',default='',type=str))