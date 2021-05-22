'''
This file shall contain initialization of the API, perform the addition of the resources, such as [Endpoint]Resource.
'''

from flask_restful import Api

api=Api()

from chathouse.rest.key_parameters import KeyParametersResource
api.add_resource(KeyParametersResource,'/api/key-parameters')

from chathouse.rest.tokens import VerificationResource,GrantResource,AccessResource
api.add_resource(VerificationResource,'/api/tokens/verification')
api.add_resource(GrantResource,'/api/tokens/grant')
api.add_resource(AccessResource,'/api/tokens/access')

from chathouse.rest.chats import IdentifiedChatResource,IdentifiedChatPublicKeysResource,IdentifiedChatMessagesResource
api.add_resource(IdentifiedChatResource,'/api/chats/<int:identification>')
api.add_resource(IdentifiedChatPublicKeysResource,'/api/chats/<int:identification>/public-keys')
api.add_resource(IdentifiedChatMessagesResource,'/api/chats/<int:identification>/messages')

from chathouse.rest.users import UsersResource,IdentifiedUserResource,IdentifiedUserParticipationsResource
api.add_resource(UsersResource,'/api/users')
api.add_resource(IdentifiedUserResource,'/api/users/<int:identification>')
api.add_resource(IdentifiedUserParticipationsResource,'/api/users/<int:identification>/participations')