'''
[Endpoint]Resource
This file shall contain defined Resource classes for this specific [Endpoint]=IdentifiedChatMessages=/api/chats/<identified>/messages:

[IdentifiedChatMessagesPublicKeys]Resource = /api/chats/<identified>/messages
'''
from chathouse.rest.chats.identified.messages.controller import GetIdentifiedChatMessagesController
from flask_restful import Resource,request

class IdentifiedChatMessagesResource(Resource):
	'''
	IdentifiedChatMessagesResource - a class, meant to handle any get requests according to the endpoint /api/chats/<identification>/messages.

	Inherits: Resource.
	
	Methods:
		get - a method defined to handle get requests aimed at the /api/chats/<id>/messages.
	'''
	def get(self,identification):
		'''
		Goal: control the handling of the get request.
		Arguments: identification:int - a chat indetification in a form of a unique inteter|numeric id.
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			GET -> GetIndentifiedChatMessagesController.handle(headers,data) -> GetIndentifiedChatMessagesStrategy.accept(headers,data,kwargs).
		Kwargs:
			identification:identifcation value of a chat
			dnt:requested latest date n time value as a GET parameter
			amount:requested amount of messages as a GET parameter
		Returns: response:tuple(JSON_Response:dict,status_code:int)
		'''
		return GetIdentifiedChatMessagesController.handle(dict(request.headers), data if (data:=request.json) else {} , identification=identification, dnt=request.args.get('dnt',default=0,type=int),amount=request.args.get('amount',default=0,type=int))