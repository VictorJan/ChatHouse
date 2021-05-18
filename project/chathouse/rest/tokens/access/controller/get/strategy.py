from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from chathouse.utilities.security.token import Token
from chathouse.service import UserService
from flask import current_app

class GetAccessStrategy(Strategy):
	'''
	GetAccessStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the GetAccessController.handle(some headers,some data)),
		Core action:
			validation:
				headers with the help of authorized decorator. 
			response:
				based on the validation come up with a respected response.
	'''

	@authorized(token_type='grant')
	def accept(self,headers,data,**kwargs):
		'''
		Goal : Generate an access token, based on the provided grant_token and it's payload.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

			headers : meant to contain all headers data , in this particular case - an Authorization|Cookie field as a sign of authority, must contain a "Bearer <token>"|"grant_token=<token>" , which is the grant_token:
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
							location:str
						}
					}
				}
			}

	 	Full verification:
	  		0.Verify the grant_token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService, and verifies the provided token_version with the current one related to the UserService :
  				If 0. is invalid respond with 401, message:"Invalid grant token.";
	  			Otherwise head to the generation phase.
  			
		Generation:
  			access_token={user_id: <owner.id>:int, token_type: "access":str, token_version: <owner.token_version>:int , dnt:float}
 
		Returns:
			If the grant token(the ownership,signature) is invalid:
  				Return 401, message:"Unauthorized!","reason":"Invalid grant token."
  			Otherwise:
  				Return 200, {access_token:<access_token>}

  		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.
		'''
	#Code:
		#Exceptions:
		assert all(map(lambda argument: isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')

		#Step 0.
		if not kwargs['authorization']['grant']['valid'] or (owner:=kwargs['authorization']['grant']['owner']) is None:
			return {'success':'False','message':'Unauthorized!','reason':'Invalid grant token.'},401
		
		return {'success':'True','access_token':Token(payload_data={'user_id':owner.id,'token_type':'access','token_version':owner.token_version,'exp':{'minutes':10}}).value},200