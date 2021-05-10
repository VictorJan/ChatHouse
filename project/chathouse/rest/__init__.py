from chathouse.rest.tokens import VerificationResource

from flask_restful import Api

api=Api()
api.add_resource(VerificationResource,'/api/tokens/verification')