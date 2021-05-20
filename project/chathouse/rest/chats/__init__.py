'''
[Endpoint]Resource
This file shall contain defined Resource classes for this specific [Endpoint]=Token=/api/chats:

[IdentifiedChat]Resource = /api/chats/<identified>
[IdentifiedChatMessages]Resource = /api/chats/<identified>/messages
[IdentifiedChatPublicKeys]Resource = /api/chats/<identified>/public-keys
'''
from chathouse.rest.chats.identified import IdentifiedChatResource
from chathouse.rest.chats.identified.public_keys import IdentifiedChatPublicKeysResource
from chathouse.rest.chats.identified.messages import IdentifiedChatMessagesResource