from chathouse.utilities.security.controller_handler.controller import Controller
from chathouse.utilities.security.controller_handler.controller import Handler
from chathouse.utilities.security.validation.headers import authorized
from chathouse.utilities.security.token import Token
from flask import render_template,redirect,url_for,current_app,make_response,request

class LogInHandler(Handler):
	
	@authorized(token_type='grant', location='Cookie')
	@authorized(token_type='preaccess', location='Cookie')
	def accept(self,headers,data,**kwargs):
		if kwargs['authorization']['grant']['valid']:
			return redirect(url_for('authorized.chat'))
		
		response=make_response(render_template('/public/auth.html',route="login"))
		
		if not kwargs['authorization']['preaccess']['valid']:
			response.set_cookie('preaccess_token',Token(payload_data={'route':'login','token_type':'preaccess','exp':{'minutes':30}}).value,httponly=True,samesite='Strict')
		
		return response
