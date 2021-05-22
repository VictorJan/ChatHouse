from chathouse.utilities.security.controller_strategy.controller import Strategy
from chathouse.utilities.security.token import Token
from chathouse.utilities.security.validation.headers import authorized
from flask import render_template,redirect,url_for,current_app,make_response,request

class VerifyStrategy(Strategy):
	'''
	Inherits:Strategy
	'''
	@authorized(token_type='verification',location='transmited-verification_token')
	@authorized(token_type='grant',location='Cookie')
	def accept(self,headers,data,**kwargs):
		'''
		Goal: validate the access to the verification page - based on the provided tokens.

		Actions:
			1.If the request contains a valid grant token, then a user is already signed in - redirect them to the authorized route.
			Otherwise proceed to the next step.
			2.If the provided headers contain a valid verification token - which is retrasmited from the url into the custom header - "transmited-verification_token" - render the requested page.
			Otherwise the verification token is invalid - redirect the client to the start route.
		'''
		if kwargs['authorization']['grant']['valid']:
			return redirect(url_for('authorized.chat'))
		if kwargs['authorization']['verification']['valid']:
			return make_response(render_template('/public/auth.html',route="verify"))
		return redirect(url_for('public.start'))
