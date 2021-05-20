from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized

class GetIdentifiedChatPublicKeysStrategy(Strategy):
	'''
	GetIdentifiedChatPublicKeysStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in theGetIdentifiedChatPublicKeysController.handle(some headers,some data)),
		Core action:
			validation:
				headers with the help of authorized decorator. 
			response:
				based on the validation come up with a respected response.
	'''

	@authorized(token_type='access',location='Authorization')
	def accept(self,headers,data,**kwargs):
		'''
		Goal : Retreive data about a specific chat, based on the provided id. The demand for the data shall be accepted , if the request constains an access token of the participant of the particular chat.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

		headers : meant to contain all headers data , in this particular case - an Authorization field as a sign of authority, must contain a "Bearer <token> , which is the access_token:
			access_token={user_id:int, token_type: "access":str, token_version:int , dnt:float}
		Note:
			This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
			To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.

		data : meant to store any data that's passed into the request - in this case, data is irrelevant:
			
		kwargs: meant to store any data passed into the accept method, from the initial requrest, up to the authorization steps. In particular stores :
		The identification at : { identification:int }
		The authorization key , which on it's own stores shall store more nested information related to a token_type.
		In this instance the token_type is the access one - so kwargs shall store:{
			authorization:{
				access:{
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
			user_keyring_payload:
				Goal: return a dictionary containing user's identifier, a keyring cotaining their public_key.
				Arguments: user:UserService. 
				Returns: dict('id':<id>,'keyring':{'public_key':<public_key>})

			public_keys_payload
				Goal: return a list containing publickeys of the participants using the user_keyring_payload.
				Arguments: participants:tuple(UserServices). 
				Returns: dict('id':<id>,'username':<username>)
			
			data_payload:
				Goal: structure and return a dictionary meant for the data key in the response.
				Arguments: chat:ChatService
				Returns: a dictionary of (id:<chat.id:int>,participants:<public_keys_payload(chat.participations):list>)

	 	Full verification:
	  		0.Verify the access_token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService, and verifies the provided token_version with the current one related to the UserService :
  			1.Verify the relationship/participation of the owner and the chat
  				If 0.|1. is invalid respond with 401, message:"Invalid access token.";
	  			Otherwise head to the generation phase.
  			
		Generation:
  			data={
	  			id:<chat's id:int>
				participants:[{id:<user's id:int>,keyring:{public_key:<key value:int>}},...]
	  		}
 
		Returns:
			If the access_token(the ownership,signature) is invalid:
  				Return 401, message:"Unauthorized!","reason":"Invalid access token."
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
		user_keyring_payload = lambda user: {'id':user.id,'keyring':{'public_key':user.keyring.public_key}}
		
		public_keys_payload = lambda participations: [ user_keyring_payload(participant) for participant in participations ] if participations else []
		
		data_payload = lambda chat: {
		'id':chat.id,
		'participants':public_keys_payload(chat.participations)
		}

		#Step 0.
		#Step 1.
		if not isinstance(kwargs['identification'],int) or not kwargs['authorization']['access']['valid'] or (owner:=kwargs['authorization']['access']['owner']) is None or (requested_chat:=owner.get_a_chat(kwargs['identification'])) is None:
			return {'success':'False','message':'Unauthorized!','reason':'Invalid access token.'},401

		return {'success':'True','data':data_payload(requested_chat)},200