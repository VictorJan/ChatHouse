from chathouse.socket.chat.controller import ConnectChatController,DisconnectChatController,Establish_a_MessageChatController,Discharge_MessagesChatController
from flask_socketio import Namespace
from flask import request

class ChatNamespace(Namespace):
	'''
	ChatNamespace - a class, meant to handle any events pointed at the endpoint /sockets/chat.

	Inherits: Resource.
	
	Methods:
		on_[event]:

		on_connect - a method defined to handle connections,handshakes, joining the room.

		on_disconnect - a method defined to handle disconnection, leaving the room.

		on_establish_a_message - a method defined to handle events related to creating/sending messages.

		on_discharge_messages - a method defined to handle events related to deleting/removing messages.
	'''
	def on_connect(self):
		'''
		Goal: control the handling of the connect event.
		
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			connect -> ConnectChatController.handle(headers,data is an empty dictionary,chat_id from the URL) -> ConnectChatStrategy.accept(headers,data,kwargs).
		
		Returns: None
		'''
		ConnectChatController.handle(dict(request.headers), {} , chat_id=request.args.get('chat_id',None,int))

	def on_disconnect(self):
		'''
		Goal: control the handling of the disconnect event.
		
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			disconnect -> DisconnectChatController.handle(headers,data is an empty dictionary,chat_id from the URL) -> DisconnectChatStrategy.accept(headers,data,kwargs).
		
		Returns: None
		'''
		DisconnectChatController.handle(dict(request.headers), {} , chat_id=request.args.get('chat_id',None,int))

	def on_establish_a_message(self,data):
		'''
		Goal: control the handling of the establish_a_message event.
		Arguments:data:dict.

		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			establish_a_message -> Establish_a_MessageChatController.handle(headers,data) -> Establish_a_MessageChatStrategy.accept(headers,data,kwargs).
		
		Returns: None
		'''
		Establish_a_MessageChatController.handle(dict(request.headers),data if isinstance(data,dict) else {}, chat_id=request.args.get('chat_id',None,int))

	def on_discharge_messages(self,data):
		'''
		Goal: control the handling of the establish_a_chat event.
		Arguments:data:dict.

		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			discharge_messages -> Establish_MessagesChatController.handle(headers,data) -> Establish_MessagesChatStrategy.accept(headers,data,kwargs).
		
		Returns: None
		'''
		Discharge_MessagesChatController.handle(dict(request.headers),data if isinstance(data,dict) else {}, chat_id=request.args.get('chat_id',None,int))


