from chathouse.utilities.security.controller_handler.controller import Handler
from chathouse.utilities.security.token import Token
from chathouse.utilities.security.validation.headers import authorized
from flask import render_template,redirect,url_for,current_app,make_response,request

class VerifyHandler(Handler):
	@authorized(token_type='preaccess',location='Cookie')
	@authorized(token_type='grant',location='Cookie')
	def accept(self,headers,data,**kwargs):
		if not kwargs['authorization']['preaccess']['valid'] or not kwargs['authorization']['grant']['valid']:
			return redirect(url_for('public.start'))
		if kwargs['authorization']['grant']['valid']:
			return redirect(url_for('authorized.chat'))
		response=make_response(render_template('/public/auth.html',route="verify"))
		return response
