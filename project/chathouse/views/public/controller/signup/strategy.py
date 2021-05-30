from chathouse.utilities.security.controller_strategy.controller import Controller
from chathouse.utilities.security.controller_strategy.controller import Strategy
from chathouse.utilities.security.validation.headers import authorized
from chathouse.utilities.security.token import Token
from flask import render_template,redirect,url_for,current_app,make_response

class SignUpStrategy(Strategy):
	'''
	SignUpStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the GetLogoutController.handle(some headers,{})),
		Core action:
			validation:
				headers with the help of authorized decorator. 
			response:
				based on the validation come up with a respective response.
	'''
	@authorized(token_type='grant', location='Cookie')
	@authorized(token_type='preaccess', location='Cookie')
	def accept(self,headers,data,**kwargs):
		'''
		Goal: validate/provide access to the signup page - based on the provided tokens.
				
		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

		headers : meant to contain all headers data , in this particular case - Cookie field as a sign of authority for the grant_token and another Cookie field for the preaccess_token:
			grant_token = {user_id: value:int, token_type: "grant":str, activity: UserService(id=value of user_id).activity , dnt:float}
			preaccess_token = {route:str('signup'),token_type:str('preaccess')}
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
				preaccess:{
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
			2.If the provided headers doesnt contain a valid preaccess token / or the route doesn't correspond the requested one - signup:
				Set the preaccess_token with proper route,type and expiration value - as a HTTPonly Cookie with samesite set to Strict. 
			Then in either way render a respective template for the requested route.

		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.
		'''
	#Code:
		#Exceptions:
		assert all(map(lambda argument: isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')

		if kwargs['authorization']['grant']['valid']:
			return redirect(url_for('authorized.chat'))
		
		response=make_response(render_template('/public/auth.html',route="signup"))
		
		if not (valid:=kwargs['authorization']['preaccess']['valid']) or kwargs['authorization']['preaccess']['token']['object']['route']!='signup' :
			response.set_cookie('preaccess_token',Token(payload_data={'route':'signup','token_type':'preaccess','exp':current_app.config['PREACCESS_EXP']}).value,httponly=True,samesite='Strict')
		
		return response
