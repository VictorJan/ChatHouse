'''
[Endpoint]Resource
This file shall contain defined Resource classes for this specific [Endpoint]=IdentifiedChatPublicKeys=/api/chats/<identified>/public-keys:

[IdentifiedChatPublicKeysPublicKeys]Resource = /api/chats/<identified>/public-keys
'''
from chathouse.rest.chats.identified.public_keys.controller import GetIdentifiedChatPublicKeysController
from flask_restful import Resource,request

class IdentifiedChatPublicKeysResource(Resource):
	'''
	IdentifiedChatPublicKeysResource - a class, meant to handle any get requests according to the endpoint /api/chats/<identification>/public-keys.

	Inherits: Resource.
	
	Methods:
		get - a method defined to handle get requests aimed at the /api/chats/<identification>/public-keys.
			Arguments: identification:int - a chat indetification in a form of a unique inteter|numeric id.
	'''
	def get(self,identification):
		'''
		Goal: control the handling of the get request.
		
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			GET -> GetIndentifiedChatPublicKeysController.handle(headers,data) -> GetIndentifiedChatPublicKeysStrategy.accept(headers,data,kwargs).
		
		Returns: response:tuple(JSON_Response:dict,status_code:int)
		'''
		return GetIdentifiedChatPublicKeysController.handle(dict(request.headers), data if (data:=request.json) else {} , identification=identification)