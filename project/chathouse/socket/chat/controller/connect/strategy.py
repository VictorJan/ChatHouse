from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from flask_socketio import join_room,disconnect

class ConnectChatStrategy(Strategy):
	'''
	ConnectChatStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the ConnectChatController.handle(some headers,some data)),
		Core action:
			validation:
				headers with the help of the authorized decorator. 
			response:
				based on the validation come up with a respective response.
	'''

	@authorized(token_type='access',location='Authorization')
	def accept(self,headers,data,**kwargs):
		'''
		Goal : Having performed a custom handshake , join a client to their notification room.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

			headers : meant to contain all headers data , in this particular case - an Authorization field as a sign of authority, must contain a "Bearer <token> , which is the access_token:
				access_token={user_id:int, token_type: "access":str, activity:int , dnt:float}
			Note:
				This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
				To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.
			
			data : meant to store any data that's passed into the request - in this case, data is irrelevant:
		  	
			kwargs: meant to store any data passed into the accept method, from the initial requrest, up to the authorization steps. In particular stores :
			The chat identification: chat_id:int
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

	 	Full verification and actions:
	  		0.Verify the access_token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService, and verifies the provided activity with the current one related to the UserService :
  			1.Verify the presense of the chat_id and existing relationship/participation of the user and/in the provided chat_id.
  				If 0.1. is invalid - disconnect the client.
	  			Otherwise join the client to a room - which is the chat_id.

  		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.
		'''
	#Code:
		#Exceptions:
		assert all(map(lambda argument: isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')

		#Step 0.
		#Step 1.
		if kwargs['chat_id'] is None or not kwargs['authorization']['access']['valid'] or (owner:=kwargs['authorization']['access']['owner']) is None or owner.get_a_chat(kwargs['chat_id']) is None:
			disconnect()
			return None
			
		join_room(kwargs['chat_id'])
		return None