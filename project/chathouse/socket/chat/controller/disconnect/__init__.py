from chathouse.socket.chat.controller.disconnect.strategy import DisconnectChatStrategy
from chathouse.utilities.security.controller_strategy.controller import Controller

'''
Initilizes a proper controller, by creating an instance of a Controller and providing an according Strategy. Thus the Controller must only call the handle method to basically handle the request based on the choosen Strategy.

Pattern/Chain of calls:
	Controller.handle(request_headers,request_data,chat_id in the kwargs) -> any decorators ( Strategy.accept(request_headers,request_data,kwargs) ).

In this case the Controller is the - [Disconnect][Chat]Controller.
[Disconnect] - an event.
[Chat] - a socket endpoint - /socket/chat.
'''

DisconnectChatController=Controller(DisconnectChatStrategy())