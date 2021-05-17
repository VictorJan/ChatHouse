from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from flask import current_app

class GetKeyParametersStrategy(Strategy):

	@authorized(token_type='verification',location='Authorization')
	def accept(self,headers,data,**kwargs):
		if kwargs['authorization']['verification']['valid']:
			return {'success':'True',**dict(zip('gm',current_app.config['DH_PARAMETERS']))},200
		return {'success':'False','message':'Unauthorized'},401
