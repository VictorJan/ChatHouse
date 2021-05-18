from chathouse.socket.chat.controller import ConnectChatController
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


	'''
	def on_connect(self):
		ConnectChatController.handle(dict(request.headers), data if (data:=request.json) is not None else {} , chat_id=request.args.get('chat_id',None))

	def on_disconnect(self):
		pass
