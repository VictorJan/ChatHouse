from chathouse.socket.notification.controller import ConnectNotificationController,DisconnectNotificationController,Establish_a_ChatNotificationController,Discharge_a_ChatNotificationController
from flask_socketio import Namespace,disconnect
from flask import request

class NotificationNamespace(Namespace):
	'''
	NotificationNamespace - a class, meant to handle any events pointed at the endpoint /sockets/notification.

	Inherits: Resource.
	
	Methods:
		on_[event]:

		on_connect - a method defined to handle connections,handshakes, joining the room.

		on_establish_a_chat - a method defined to handle notifications related to starting new chats.

		on_discharge_a_chat - a method defined to handle notifications related to removing chats.

		on_disconnect - a method defined to handle disconnection, leaving the room.
	'''
	def on_connect(self):
		'''
		Goal: control the handling of the connect event.
		
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			connect -> ConnectNotificationController.handle(headers,data is an empty dictionary) -> ConnectNotificationStrategy.accept(headers,data,kwargs).
		
		Returns: None
		'''
		ConnectNotificationController.handle(dict(request.headers),{})

	def on_disconnect(self):
		'''
		Goal: control the handling of the disconnect event.
		
		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			disconnect -> DisconnectNotificationController.handle(headers,data is an empty dictionary) -> DisconnectNotificationStrategy.accept(headers,data,kwargs).
		
		Returns: None
		'''
		DisconnectNotificationController.handle(dict(request.headers),{})

	def on_establish_a_chat(self,data={}):
		'''
		Goal: control the handling of the establish_a_chat event.
		Arguments:data:dict.

		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			establish_a_chat -> Establish_a_ChatNotificationController.handle(headers,data) -> Establish_a_ChatNotificationStrategy.accept(headers,data,kwargs).
		
		Returns: None
		'''
		Establish_a_ChatNotificationController.handle(dict(request.headers), data if isinstance(data,dict) else {} )

	def on_discharge_a_chat(self,data={}):
		'''
		Goal: control the handling of the discharge_a_chat event.
		Arguments:data:dict.

		Actions: By using the defined pattern, perform the handle method of the proper Controller, which would use defined Strategy to accept the request headers and data:
			discharge_a_chat -> Discharge_a_ChatNotificationController.handle(headers,data) -> Discharge_a_ChatNotificationStrategy.accept(headers,data,kwargs).
		
		Returns: None
		'''
		Discharge_a_ChatNotificationController.handle(dict(request.headers),data if isinstance(data,dict) else {} )
