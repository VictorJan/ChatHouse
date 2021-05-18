'''
[Endpoint]Resource
This file shall contain defined Resource classes for this specific [Endpoint]=IdentifiedChat=/api/chats/<identified>:

[IdentifiedChat]Resource = /api/chats/<identified>
[IdentifiedChatMessages]Resource = /api/chats/<identified>/messages
[IdentifiedChatPublicKeys]Resource = /api/chats/<identified>/public-keys
'''

from flask_restful import Resource,request

class IdentifiedChatResource(Resource):
	'''
	IdentifiedChatResource - a class, meant to handle any get requests according to the endpoint /api/chats/<identified>.

	Inherits: Resource.
	
	Methods:
		get - a method defined to handle get requests aimed at the /api/chats/<id>.
			Arguments: identification:int - a chat indetification in a form of a unique inteter|numeric id.
	'''
	def get(self,identification):
		'''
		Goal: control the handling of the get request.
		
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			GET -> GetIndentifiedChatController.handle(headers,data) -> GetIndentifiedChatStrategy.accept(headers,data,kwargs).
		
		Returns: response:tuple(JSON_Response:dict,status_code:int)
		'''
		return GetIndentifiedChatController.handle(dict(request.headers), data if isinstance((data:=request.json),dict) else {} , chat_id=identification)