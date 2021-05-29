from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from flask import current_app

class GetIdentifiedUserKeyringStrategy(Strategy):
	'''
	GetIdentifiedUserKeyringStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the GetIdentifiedUserKeyringController.handle(some headers,some data)),
		Core action:
			validation:
				headers with the help of authorized decorator. 
			response:
				based on the validation come up with a respective response.
	'''
	
	@authorized(token_type='confirmation',location='Authorization')
	@authorized(token_type='access',location='Authorization')
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
				access:{
					valid:bool,
					status:int,
					owner:UserService|None,
					token:{
						object:None|Token,
						location:str|None
					}
				confirmation:{
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

		Lambda functions:

			keyring_payload:
				Goal: return a dictionary, which contains public and private keys from the keyring and related infromation, such as g and m.
				Arguments: keyring:KeyringService. 
				Returns: list(for each chat <chat_payload(chat):dict>,...) if keyring is not empty, otherwise list(Empty)

			data_payload:
				Goal: structure and return a dictionary meant for the data key in the response.
				Arguments: requester:UserService - the owner of the access|confirmation token.
				Returns: a dictionary of (keyring:<keyring_payload(requester.keyring):dict>)

			resolve:
				Goal: try to find a valid token (signature and ownership) , based on the implemented-allowed ones: access,confirmation.
				Arguments: authorizations:tuple - meant to store the provided authorization resolutions for the access and the confirmation token.
				Actions: iterate through the authorizations until any of them have been established as valid , with an existing proper owner , then return such case, otherwise provide a None as a feedback.
				Returns: token:dict if any token(confirmation,access) has been fully valid otherwise None. 

	 	Full verification:
	  		0.Resolve the provided authority - the token, verifying the token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService,
	  		and verifies the provided activity with the current one related to the UserService. Apart from that resolution - makes sure of the relation of the requester's id  and the requested user's id. 
  				If 0. is invalid respond with 401, message:"Invalid access|confirmation token.";
	  			Otherwise head to the generation phase.
	  		
		Generation:
  			data={
					keyring:
						{
							private_key:dict(an encrypted private key - dict(iv:str,data:str)),
							public_key:int
						},
					parameters:
						{
							g:int(primitive element),
							m:int(modulus)
						}
				}
 
		Returns:
			If the access|confirmation_token(the ownership,signature) is invalid or the owner's id is not equal to the one provided in the URL:
  				Return 401, message:"Unauthorized!","reason":"Invalid access|confirmation token."
  			Otherwise:
  				Return 200, data:<data_payload>

  		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.
  				TyperError - if the identification argument is not provided or the datatype of the value is not an integer.
		'''
	#Code:
		#Exceptions:
		assert all(map(lambda argument: isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')
		assert isinstance(kwargs.get('identification',None),int), TypeError('The identification argument hasn\'t been submited or the data type is invalid.')
		
		#Lambda functions:
		
		resolve = lambda *authorizations: token if any((token:=case) for case in authorizations if case['valid'] and case['owner'] is not None and case['owner'].id==kwargs['identification']) else None

		keyring_payload = lambda keyring: {\
		'keyring':{'private_key':keyring.private_key, 'public_key':keyring.public_key},\
		'parameters': { **dict(zip('gm',current_app.config['DH_PARAMETERS']))\
		}}
		
		data_payload = lambda requester: keyring_payload(requester.keyring)
		
		#Step 0.
		if (token:=resolve(kwargs['authorization']['access'],kwargs['authorization']['confirmation'])) is None:
			return {'success':'False','message':'Unauthorized!','reason':f"Invalid access|confirmation token."},401

		return {'success':'True','data':data_payload(token['owner'])},200