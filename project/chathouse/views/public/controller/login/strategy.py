from chathouse.utilities.security.controller_strategy.controller import Controller
from chathouse.utilities.security.controller_strategy.controller import Strategy
from chathouse.utilities.security.validation.headers import authorized
from chathouse.utilities.security.token import Token
from flask import render_template,redirect,url_for,current_app,make_response

class LogInStrategy(Strategy):
	
	@authorized(token_type='grant', location='Cookie')
	@authorized(token_type='preaccess', location='Cookie')
	def accept(self,headers,data,**kwargs):
		if kwargs['authorization']['grant']['valid']:
			return redirect(url_for('authorized.chat'))
		
		response=make_response(render_template('/public/auth.html',route="login"))
		
		if not kwargs['authorization']['preaccess']['valid'] or kwargs['authorization']['preaccess']['token']['object']['route']!='login':
			response.set_cookie('preaccess_token',Token(payload_data={'route':'login','token_type':'preaccess','exp':current_app.config['PREACCESS_EXP']}).value,httponly=True,samesite='Strict')
		
		return response
