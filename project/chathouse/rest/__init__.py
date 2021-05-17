'''
This file shall contain initialization of the API, perform the addition of the resources, such as [Endpoint]Resource.
'''
from chathouse.rest.tokens import VerificationResource,GrantResource
from chathouse.rest.key_parameters import KeyParametersResource

from flask_restful import Api

api=Api()
api.add_resource(KeyParametersResource,'/api/key-parameters')
api.add_resource(VerificationResource,'/api/tokens/verification')
api.add_resource(GrantResource,'/api/tokens/grant')
