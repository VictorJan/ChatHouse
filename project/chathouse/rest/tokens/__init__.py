'''
[Endpoint]Resource
This file shall contain defined Resource classes for this specific [Endpoint]=Token=/api/tokens:
[Verification]Resource = /api/tokens/verification
[Grant]Resource = /api/tokens/grant
'''
from chathouse.rest.tokens.verification import VerificationResource
from chathouse.rest.tokens.grant import GrantResource