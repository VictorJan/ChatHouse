'''
[Method][Endpoint]Controller
This file shall contain Controllers for each [Method]:
Get=GET for this specific [Endpoint]=IdentifiedUser=/api/users/<identification>.
Put=PUT for this specific [Endpoint]=IdentifiedUser=/api/users/<identification>.
Delete=DELETE for this specific [Endpoint]=IdentifiedUser=/api/users/<identification>.
'''
from chathouse.rest.users.identified.controller.get import GetIdentifiedUserController
from chathouse.rest.users.identified.controller.put import PutIdentifiedUserController
from chathouse.rest.users.identified.controller.delete import DeleteIdentifiedUserController