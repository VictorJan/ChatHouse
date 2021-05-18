from chathouse.utilities.security.controller_strategy.controller import Strategy
from chathouse.utilities.security.token import Token
from chathouse.utilities.security.validation.headers import authorized
from flask import render_template,redirect,url_for,current_app,make_response,request

class VerifyStrategy(Strategy):
	#@authorized(token_type='preaccess',location='Cookie')
	@authorized(token_type='grant',location='Cookie')
	def accept(self,headers,data,**kwargs):
		#if not kwargs['authorization']['preaccess']['valid']:
		#	return redirect(url_for('public.start'))
		if kwargs['authorization']['grant']['valid']:
			return redirect(url_for('authorized.chat'))
		if (verification_token:=Token(raw_data=kwargs['verification_token'])).is_valid:
			return make_response(render_template('/public/auth.html',route="verify"))

		return redirect(url_for('public.start'))
