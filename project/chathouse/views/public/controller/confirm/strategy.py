from chathouse.utilities.security.controller_strategy.controller import Strategy
from chathouse.utilities.security.token import Token
from chathouse.utilities.security.validation.headers import authorized
from flask import render_template,redirect,url_for

class ConfirmStrategy(Strategy):
	'''
	ConfirmStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the GetLogoutController.handle(some headers,{})),
		Core action:
			validation:
				headers with the help of authorized decorator. 
			response:
				based on the validation come up with a respective response.
	'''
	@authorized(token_type='confirmation',location='transmited-confirmation_token')
	@authorized(token_type='grant',location='Cookie')
	def accept(self,headers,data,**kwargs):
		'''
		Goal: validate the access to the confirmation page - based on the provided tokens.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

		headers : meant to contain all headers data , in this particular case - Cookie field as a sign of authority for the grant_token and the explicitly set transmited-veirification_token field for the verification_token:
			grant_token = {user_id: value:int, token_type:str('grant'), activity: UserService(id=value of user_id).activity , dnt:float}
			confirmation_token = {user_id: value:int, token_type:str('confirmation'), action:str('delete'|'put'), activity: UserService(id=value of user_id).activity , dnt:float}

		Note:
			This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
			To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.
		
		data : meant to store any data that's passed into the request - in this case data is irrelevant:
	  	
		kwargs: meant to store any data passed into the accept method, from the initial requrest, up to the authorization steps. In particular stores the authorization key , which on it's own shall store nested information related to a token_type.
		In this instance the token_type could be the grant or the verification one - so kwargs shall store:{
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
				verification:{
					valid:bool,
					status:int,
					token:{
						object:None|Token,
						location:str|None
					}
				}
			}
		}
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
