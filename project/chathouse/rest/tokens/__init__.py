'''
[Endpoint]Resource
This file shall contain defined Resource classes for this specific [Endpoint]=Token=/api/tokens:
[Verification]Resource = /api/tokens/verification
[Grant]Resource = /api/tokens/grant
[Access]Resource = /api/tokens/access
[Confirmation]Resource = /api/tokens/confirmation
'''
from chathouse.rest.tokens.verification import VerificationResource
from chathouse.rest.tokens.grant import GrantResource
from chathouse.rest.tokens.access import AccessResource
from chathouse.rest.tokens.confirmation import ConfirmationResource