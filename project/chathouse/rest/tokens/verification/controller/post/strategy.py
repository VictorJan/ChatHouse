from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from chathouse.rest.tokens.verification.controller.post.template import IDSignUpVerificationTemplate,IDLogInVerificationTemplate

class PostVerificationStrategy(Strategy):

	@authorized(token_type='preaccess')
	def accept(self,headers,data,**kwargs):
		if not kwargs['authorization']['preaccess']['valid']:
			return {'message':'Unauthorized!'},401
		template = IDSignUpVerificationTemplate if (route:=kwargs['authorization']['preaccess']['token']['object']['route']=='signup') else IDLogInVerificationTemplate
		if isinstance(data,dict) and template.validate(**data):
			data=template.data
			return {'message':'Email has been sent'},200
		else:
			return {'message':'Invalid data'},400

