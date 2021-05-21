from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from flask import redirect,url_for,make_response,render_template
import datetime

class ChatStrategy(Strategy):

	@authorized(token_type='grant')
	def accept(self,headers,data,**kwargs):

		if not kwargs['authorization']['grant']['valid'] or (owner:=kwargs['authorization']['grant']['owner']) is None \
		or ( ( (chat:=owner.get_a_chat(int(kwargs['chat_id']))) is None if kwargs['chat_id'].isnumeric() else True ) if kwargs['chat_id'] is not None else False ) :
			return redirect(url_for('public.start'))

		response=make_response(render_template('authorized/chat.html',current_user=kwargs['authorization']['grant']['owner'],current_chat = chat if kwargs['chat_id'] is not None else None))

		response.delete_cookie('preaccess_token')

		if kwargs['authorization']['grant']['token']['location']=='Authorization':
			response.set_cookie('grant_token',kwargs['authorization']['grant']['token']['object'].value,\
				expires=datetime.datetime.fromtimestamp(kwargs['authorization']['grant']['token']['object']['exp']),\
				httponly=True,samesite='Strict')
		return response

