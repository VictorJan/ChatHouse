from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from flask import current_app

class GetKeyParametersStrategy(Strategy):
	'''
	GetKeyParametersStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the GetKeyParametersController.handle(some headers,some data)),
		Core action:
			validation:
				headers with the help of authorized decorator. 
			response:
				based on the validation come up with a respective response.
	'''

	@authorized(token_type='verification',location='Authorization')
	def accept(self,headers,data,**kwargs):
		'''
		Goal : Retreive the keyring data of the provided user, having provided a respective authority - access token , ownership of which references the requested user.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

		headers : meant to contain all headers data , in this particular case - an Authorization field as a sign of authority, must contain a "Bearer <token> , which could be the access_token or the confirmation_token:
			access_token={user_id:int, token_type:str("access"), activity:int , dnt:float}
			confirmation_token={user_id:int, action:str("put"|"delete") token_type:str("confirmation"), activity:int , dnt:float}
		Note:
			This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
			To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.

		data : meant to store any data that's passed into the request - in this case, data is irrelevant:
			
		kwargs: meant to store any data passed into the accept method, from the initial requrest, up to the authorization steps. In particular stores :
		The identification at : { identification:int }
		In this instance the token_type is the access|confirmation one - so kwargs shall store:{
			authorization:{
				verification:{
					valid:bool,
					status:int,
					token:{
						object:None|Token,
						location:str|None
					}
				}
			}

	 	Full verification:
	  		If the verification token is invalid respond the 401, otherwise return a 200 , providing a generator and a modulus value - for the DiffieHellman keyrings.
		Returns:
			If the verification token is invalid(according to the signature , or the activity state):
  				Return 401, message:"Unauthorized!","reason":"Invalid veirification token."
  			Otherwise:
  				Return 200, data:<data_payload>

  		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.
  				TyperError - if the identification argument is not provided or the datatype of the value is not an integer.
		'''
		if kwargs['authorization']['verification']['valid']:
			return {'success':'True',**dict(zip('gm',current_app.config['DH_PARAMETERS']))},200
		return {'success':'False','message':'Unauthorized','reason':'Invalid verification token.'},401
