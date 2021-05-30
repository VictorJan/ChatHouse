from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from flask import redirect,url_for,make_response,render_template
import datetime

class ChatStrategy(Strategy):
	'''
	ChatStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the GetLogoutController.handle(some headers,{})),
		Core action:
			validation:
				headers with the help of authorized decorator. 
			response:
				based on the validation come up with a respective response.
	'''
	@authorized(token_type='grant')
	def accept(self,headers,data,**kwargs):
		'''
		Goal : validate access to the authorized chat view.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

			headers : meant to contain all headers data , in this particular case - Any field as a sign of authority, which is the grant_token:
				grant_token = {user_id:int(user's id), token_type:str("grant"), activity:int(UserService(id=value of user_id).activity) , dnt:float}
			Note:
				This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
				To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.
			
			data : meant to store any data that's passed into the request - in this case data is irrelevant:
		  	
			kwargs: meant to store any data passed into the accept method, from the initial requrest, up to the authorization steps. In particular stores the authorization key , which on it's own stores shall store more nested information related to a token_type.
			In this instance the token_type is the grant one - so kwargs shall store:{
				authorization:{
					grant:{
						valid:bool,
						status:int,
						owner:UserService|None,
						token:{
							object:None|Token,
							location:str|None
						}
					}
				}
			}

	 	Full actions:
	  		0.Verify the grant_token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService, and verifies the provided activity with the current one related to the UserService :
  			1.If the reuqest is aimed at a certain chat, providing a respective id - make sure that the owner is a participant of the chat. 
  				If 0.|1. is invalid, redirect the client to the start view;
	  		2.Prepare a respective render template according to the view.
	  		3.Clear the preaccess_token cookie.
	  		4.If the grant_token has been provided in the Authoriztion Field [integral part of the authentication flow] - then set the provided grant token as a strict,HTTPonly cookie - which expires at the same time as the token does.
			5.Return the prepared response. 
  			
  		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.
		'''
	#Code:
		#Exceptions:
		assert all(map(lambda argument: isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')

		if not kwargs['authorization']['grant']['valid'] or (owner:=kwargs['authorization']['grant']['owner']) is None \
		or  ( (chat:=owner.get_a_chat(int(kwargs['chat_id']))) is None if kwargs['chat_id'] is not None else False ) :
			return redirect(url_for('public.start'))

		response=make_response(render_template('authorized/chat.html',current_user=kwargs['authorization']['grant']['owner'],current_chat = chat if kwargs['chat_id'] is not None else None))

		response.delete_cookie('preaccess_token')

		if kwargs['authorization']['grant']['token']['location']=='Authorization':
			response.set_cookie('grant_token',kwargs['authorization']['grant']['token']['object'].value,\
				expires=kwargs['authorization']['grant']['token']['object']['exp'],\
				httponly=True,samesite='Strict')
		return response

