from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from chathouse.utilities.security.token import Token
from chathouse.service import UserService
from flask import current_app

class GetIdentifiedChatStrategy(Strategy):
	'''
	GetIdentifiedChatStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in theGetIdentifiedChatController.handle(some headers,some data)),
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
		The chat_id at : { chat_id:int }
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


	 	Full verification:
	  		0.Verify the access_token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService, and verifies the provided token_version with the current one related to the UserService :
  			1.Verify the relationship/participation of the owner and the chat
  				If 0. is invalid respond with 401, message:"Invalid grant token.";
	  			Otherwise head to the generation phase.
  			
		Generation:
  			chat_data={user_id: <owner.id>:int, token_type: "access":str, token_version: <owner.token_version>:int , dnt:float}
 
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
		if not kwargs['chat_id'].isnumeric() or not kwargs['authorization']['access']['valid'] or (owner:=kwargs['authorization']['access']['owner']) is None or (chat:=owner.get_a_chat(kwargs['chat_id'])) is None:
			return {'success':'False','message':'Unauthorized!','reason':'Invalid access token.'},401
		#chat_data={'id':chat.id,'name':chat.name,'participants':}
		return {'success':'True','data':{'id':chat.id,'name':chat.name,'participants':[]}},200