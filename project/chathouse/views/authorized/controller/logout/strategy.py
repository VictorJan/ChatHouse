from chathouse.utilities.security.controller_strategy.controller import Controller
from chathouse.utilities.security.controller_strategy.controller import Strategy
from chathouse.utilities.security.validation.headers import authorized
from flask import redirect,url_for,make_response

class LogoutStrategy(Strategy):
	'''
	GetLogoutStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the GetLogoutController.handle(some headers,{})),
		Core action:
			validation:
				headers with the help of authorized decorator. 
			response:
				based on the validation come up with a respective response.
	'''

	@authorized(token_type='grant',location='Cookie')
	def accept(self,headers,data,**kwargs):
		'''
		Goal : Come to a proper conclusion aim at the logout process .

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

			headers : meant to contain all headers data , in this particular case - Cookie field as a sign of authority, which is the grant_token:
				grant_token = {user_id: value:int, token_type: "grant":str, token_version: UserService(id=value of user_id).token_version , dnt:float}
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
	  		0.Verify the grant_token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService, and verifies the provided token_version with the current one related to the UserService :
  				If 0. is invalid, set status_code to 303;
	  		1.Otherwise set status_code to 302.
			2.Clear cookies, return a redirect to /start with proper status_code. 
  			
		Logout:
			Clear the samesite grant_token cookie - in either way, however :
			if the grant_token is invalid let the client know this , by giving the 303 - the see other resource 
			Otherwise the grant_token was valid , and let the user know to accordinly move to the "found" (/start) page - 302.

		Returns:
			If the grant token(the ownership,signature) is invalid:
  				set status code to 303 - to see other route, implying that the token was invalid.
  			Otherwise:
  				set status code to 302 - to see the found proper route, implying that the token was valid.
  			Clear cookies and return the redirect to /start with the derived status_code.

  		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.
		'''
	#Code:
		#Exceptions:
		assert all(map(lambda argument: isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')

		#Step 0.
		#Step 1.
		status_code = 303 if (not kwargs['authorization']['grant']['valid'] or (owner:=kwargs['authorization']['grant']['owner']) is None or not owner.update_activity() ) else 302
		response=make_response(redirect(url_for('public.start'),code=302))
		#Step 2.
		response.delete_cookie('grant_token')
		
		return response