'''
This file shall contain initialization of the Socket Service, perform the addition of the Namescapes, such as [Endpoint]Namespace.
'''
from chathouse.socket.notification import NotificationNamespace
from chathouse.socket.chat import ChatNamespace
from flask_socketio import SocketIO

socket=SocketIO()
socket.on_namespace(NotificationNamespace('/socket/notification'))
socket.on_namespace(ChatNamespace('/socket/chat'))