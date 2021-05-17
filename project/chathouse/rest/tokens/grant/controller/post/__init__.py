from chathouse.rest.tokens.grant.controller.post.strategy import PostGrantStrategy
from chathouse.utilities.security.controller_strategy.controller import Controller

'''
Initilizes a proper controller, by creating an instance of a Controller and providing an according Strategy. Thus the Controller must only call the handle method to basically handle the request based on the choosen Strategy.

Pattern/Chain of calls:
	Controller.handle(request_headers,request_data) -> any decorators ( Strategy.accept(request_headers,request_data,kwargs) ).

In this case the Controller is the - [Post][Grant]Controller.
[Post] - method POST.
[Grant] - REST endpoint - /tokens/grant.

'''
PostGrantController=Controller(PostGrantStrategy())