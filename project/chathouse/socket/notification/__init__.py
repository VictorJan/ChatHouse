from chathouse.socket.notification.controller import ConnectNotificationController,Establish_a_ChatNotificationController
from flask_socketio import Namespace
from flask import request

class NotificationNamespace(Namespace):
	'''
	NotificationNamespace - a class, meant to handle any events pointed at the endpoint /sockets/notification.

	Inherits: Resource.
	
	Methods:
		on_[event]:

		on_connect - a method defined to handle connections,handshakes, joining the room.

		on_start_chat - a method defined to handle notifications related to starting new chats.

		on_disconnect - a method defined to handle disconnection, leaving the room.


	'''
	def on_connect(self):
		ConnectNotificationController.handle(dict(request.headers), data if (data:=request.json) is not None else {} )

	def on_establish_a_chat(self,data):
		'''
		data:dict
		'''
		Establish_a_ChatNotificationController.handle(dict(request.headers), data if isinstance(data,dict) else {} )

	def on_disconnect(self):
		pass
