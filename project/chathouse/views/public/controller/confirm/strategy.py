from chathouse.utilities.security.controller_strategy.controller import Strategy
from chathouse.utilities.security.token import Token
from chathouse.utilities.security.validation.headers import authorized
from flask import render_template,redirect,url_for

class ConfirmStrategy(Strategy):
	'''
	Inherits:Strategy
	'''
	@authorized(token_type='confirmation',location='transmited-confirmation_token')
	@authorized(token_type='grant',location='Cookie')
	def accept(self,headers,data,**kwargs):
		'''
		Goal: validate the access to the confirmation page - based on the provided tokens.

		Actions:
			1.If the request contains a valid grant token, then a user is already signed in - redirect them to the authorized route.
			Otherwise proceed to the next step.
			2.If the provided headers contain a valid confirmation token - which is retrasmited from the url into the custom header - "transmited-confirmation_token" - render the requested page.
			Otherwise the confirmation token is invalid - redirect the client to the start route.
		Returns:redirect|render_template
			If a grant token, that could be found in a cookie, is valid - redirect for "authorized.chat"
			Otherwise if the confirmation token is valid - render an appropriate page.
			Otherwise redirect to the start page.
		'''
		if kwargs['authorization']['grant']['valid']:
			return redirect(url_for('authorized.chat'))
		if (confirmation_token:=kwargs['authorization']['confirmation'])['valid']:
			return render_template('/public/auth.html',route="confirm", action=confirmation_token['token']['object']['action'])
		return redirect(url_for('public.start'))
