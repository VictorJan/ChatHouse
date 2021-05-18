from chathouse.socket.chat.controller.connect.strategy import ConnectChatStrategy
from chathouse.utilities.security.controller_strategy.controller import Controller

'''
Initilizes a proper controller, by creating an instance of a Controller and providing an according Strategy. Thus the Controller must only call the handle method to basically handle the request based on the choosen Strategy.

Pattern/Chain of calls:
	Controller.handle(request_headers,request_data) -> any decorators ( Strategy.accept(request_headers,request_data,kwargs) ).

In this case the Controller is the - [Connect][Chat]Controller.
[Connect] - an event.
[Chat] - a socket endpoint - /socket/chat.
'''

ConnectChatController=Controller(ConnectChatStrategy())