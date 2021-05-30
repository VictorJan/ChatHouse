from chathouse.utilities.security.controller_strategy.controller import Controller
from chathouse.views.public.controller.verify.strategy import VerifyStrategy
'''
Initilizes a proper controller, by creating an instance of a Controller and providing an according Strategy. Thus the Controller must only call the handle method to basically handle the request based on the choosen Strategy.

Pattern/Chain of calls:
	Controller.handle(request_headers,request_data - empty) -> any decorators ( Strategy.accept(request_headers,request_data - empty,kwargs) ).

In this case the View Controller has to be GET - [Verify]Controller.
[Verify] - view route - /verify/<string:token>.
'''

VerifyController=Controller(VerifyStrategy())