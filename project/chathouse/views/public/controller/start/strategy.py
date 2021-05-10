from chathouse.utilities.security.controller_strategy.controller import Controller
from chathouse.utilities.security.controller_strategy.controller import Strategy
from chathouse.utilities.security.validation.headers import authorized
from flask import render_template,redirect,url_for

class StartStrategy(Strategy):
	@authorized(token_type='grant',location='Cookie')
	def accept(self,headers,data,**kwargs):
		if kwargs['authorization']['grant']['valid']:
			return redirect(url_for('authorized.chat'))
		return render_template('/public/start.html')