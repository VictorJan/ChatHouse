from chathouse.utilities.security.controller_strategy.controller import Strategy
from chathouse.utilities.security.token import Token
from chathouse.utilities.security.validation.headers import authorized
from flask import render_template,redirect,url_for,current_app,make_response,request

class VerifyStrategy(Strategy):
	'''
	VerifyStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the GetLogoutController.handle(some headers,{})),
		Core action:
			validation:
				headers with the help of authorized decorator. 
			response:
				based on the validation come up with a respective response.
	'''
	@authorized(token_type='verification',location='transmited-verification_token')
	@authorized(token_type='grant',location='Cookie')
	def accept(self,headers,data,**kwargs):
		'''
		Goal: validate access to the verification page - based on the provided tokens.
				
		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

		headers : meant to contain all headers data , in this particular case - Cookie field as a sign of authority for the grant_token and the explicitly set transmited-veirification_token field for the verification_token:
			grant_token = {user_id: value:int, token_type: "grant":str, activity: UserService(id=value of user_id).activity , dnt:float}
			verification_token = {identification_data:<identification_data>,token_type:"verification",activity:int,dnt:float,preaccess:<preaccess_token>}
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
			2.If the provided headers contain a valid verification token - which is retransmited from the url into the custom header - "transmited-verification_token" - render the requested page.
			Otherwise the verification token is invalid - redirect the client to the start route.

		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.
		'''
	#Code:
		#Exceptions:
		assert all(map(lambda argument: isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')

		if kwargs['authorization']['grant']['valid']:
			return redirect(url_for('authorized.chat'))
		if kwargs['authorization']['verification']['valid']:
			return make_response(render_template('/public/auth.html',route="verify"))
		return redirect(url_for('public.start'))
