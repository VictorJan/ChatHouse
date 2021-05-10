from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from flask import redirect,url_for,make_response,render_template

class ChatStrategy(Strategy):

	@authorized(token_type='grant')
	def accept(self,headers,data,**kwargs):
		if not kwargs['authorization']['grant']['valid']:
			return redirect(url_for('public.start'))
		response=render_template('authorized/chat.html')
		if kwargs['authorization']['grant']['token']['location']=='Cookie':
			response.set_cookie('grant_token',kwargs['authorization']['grant']['token']['object'].value,httponly=True,samesite='Strict')
		return response

