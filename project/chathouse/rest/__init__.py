'''
This file shall contain initialization of the API, perform the addition of the resources, such as [Endpoint]Resource.

Structure for each Resource:
Resource
|-controller
| |-[method]
| | |-strategy.py - contains a respective custom Strategy class.
| | |-template.py - (absent with GET methods) contains a "built" template for validating incoming data using Template and Field Builders.
| | |-__init__.py - contains fully configured Controller - using the implemented Strategy.
| |-__init__.py - contains "references"/improted implemeted controllers for the defined [method]s.
|-__init__.py - contains imported controllers from the controller package.
Note:
For the Strategy pattern - each controller [handle]s the request -> based on a respective Strategy , which [accept]s the data and using the explicitly enacted custom Template validates the data.
For the Builder pattern - each Template is constructed of Fields, which on its own are built using the Requirements.
[To learn more about each Strategy,Template view the respective files at [method]/strategy.py|template.py]
[To learn more about the Builder Patterns and the Requirement classes , view the files at chathouse/utilities/security/validation/data/*]
'''

from flask_restful import Api

api=Api()

from chathouse.rest.key_parameters import KeyParametersResource
api.add_resource(KeyParametersResource,'/api/key-parameters')

from chathouse.rest.tokens import VerificationResource,GrantResource,AccessResource,ConfirmationResource
api.add_resource(VerificationResource,'/api/tokens/verification')
api.add_resource(GrantResource,'/api/tokens/grant')
api.add_resource(AccessResource,'/api/tokens/access')
api.add_resource(ConfirmationResource,'/api/tokens/confirmation')

from chathouse.rest.chats import IdentifiedChatResource,IdentifiedChatPublicKeysResource,IdentifiedChatMessagesResource
api.add_resource(IdentifiedChatResource,'/api/chats/<int:identification>')
api.add_resource(IdentifiedChatPublicKeysResource,'/api/chats/<int:identification>/public-keys')
api.add_resource(IdentifiedChatMessagesResource,'/api/chats/<int:identification>/messages')

from chathouse.rest.users import UsersResource,IdentifiedUserResource,IdentifiedUserKeyringResource,IdentifiedUserParticipationsResource
api.add_resource(UsersResource,'/api/users')
api.add_resource(IdentifiedUserResource,'/api/users/<int:identification>')
api.add_resource(IdentifiedUserKeyringResource,'/api/users/<int:identification>/keyring')
api.add_resource(IdentifiedUserParticipationsResource,'/api/users/<int:identification>/participations')