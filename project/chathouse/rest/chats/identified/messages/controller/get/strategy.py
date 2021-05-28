from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from datetime import datetime

class GetIdentifiedChatMessagesStrategy(Strategy):
	'''
	GetIdentifiedChatMessagesStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in theGetIdentifiedMessagesController.handle(some headers,some data)),
		Core action:
			validation:
				headers with the help of authorized decorator. 
			response:
				based on the validation come up with a respective response.
	'''

	@authorized(token_type='access',location='Authorization')
	def accept(self,headers,data,**kwargs):
		'''
		Goal : Retreive data about a specific chat, based on the provided id. The demand for the data shall be accepted , if the request constains an access token of the participant of the particular chat.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

		headers : meant to contain all headers data , in this particular case - an Authorization field as a sign of authority, must contain a "Bearer <token> , which is the access_token:
			access_token={user_id:int, token_type: "access":str, activity:int , dnt:float}
		Note:
			This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
			To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.

		data : meant to store any data that's passed into the request - in this case, data is irrelevant:
			
		kwargs: meant to store any data passed into the accept method, from the initial requrest, up to the authorization steps. In particular stores :
		The identification at : { identification:int }
		The amount of messages at {amount:int}
		The dnt at {dnt:int} - if None , the value would be set as the default date
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
			query_payload:
				Goal: set up a part of a payload for the search of the messages.
				Arguments: data:dict, key:str. In this case would accept the data to be kwargs and key to be either amount,dnt
				Returns: a dictionary of key:data[key] if the value of the key was greater than zero - basically if the converted provided value was valid, otherwise return empty dictionary.

			sender_payload:
				Goal: return a dictionary containing some unique information about the sender of the message.
				Arguments: sender:UserService. 
				Returns: dict('id':<id>,'username':<username>)

			message_payload:
				Goal: return a dictionary containing information about a message.
				Arguments: message:MessageService. 
				Returns: dict(id:<message id:int>,content:dict(iv:str,data:str),dnt:dict(timestamp:int,readable:str),sender:sender_payload(<message.sender>))

			messages_payload:
				Goal: return a list containing messages, each payload of which is generated using message_paylaod.
				Arguments: messages: tuple(UserServices). 
				Returns: list of (message_payload(of each message in the messages)) if the messages are not None else empty list.

			data_payload:
				Goal: structure and return a dictionary meant for the data key in the response.
				Arguments: chat:ChatService
				Returns: a dictionary of (id:<chat.id:int>,messages:<messages_payload(chat.get_messages(query data)):list>)

	 	Full verification:
	  		0.Verify the access_token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService, and verifies the provided token_version with the current one related to the UserService :
  			1.Verify the relationship/participation of the owner and the chat
  				If 0.|1. is invalid respond with 401, message:"Invalid access token.";
	  			Otherwise head to the generation phase.
	  		Note if the query parameters are invalid/None - query sets them as default : current date n' time and 15 for the amount.
  			
		Generation:
  			data={
	  			id:<chat's id:int>,
				messages:[{
					id:<message id:int>
					content:{ iv:<iv:str> , data:<data:str> },
					sender:{id:<sender's id:int>, username:<sender's username:str>}
					dnt: { timestamp:<timestamp value:int>, readable:<visually comprehensible:str> }
				},...]
	  		}
 
		Returns:
			If the access_token(the ownership,signature) is invalid:
  				Return 401, message:"Unauthorized!","reason":"Invalid access token."
  			Otherwise:
  				Return 200, data:<chat_data>

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
		
		query_payload = lambda data,key: {key:data[key]} if data.get(key,0)>0 else {}

		sender_payload = lambda sender: {'id':sender.id,'username':sender.username}

		message_payload = lambda message: {'id':message.id, 'content':message.content, 'dnt':{'timestamp':int(datetime.timestamp(message.dnt)), 'readable':str(message.dnt.time()) }, 'sender':sender_payload(message.sender)}
		
		messages_payload = lambda messages: [ message_payload(message) for message in messages ] if messages else []
		
		data_payload = lambda chat: {\
		'id':chat.id,\
		'messages':messages_payload(chat.get_message(**query_payload(kwargs,'dnt'),**query_payload(kwargs,'amount')))\
		}

		#Step 0.
		#Step 1.
		if not isinstance(kwargs['identification'],int) or not kwargs['authorization']['access']['valid'] or (owner:=kwargs['authorization']['access']['owner']) is None or (requested_chat:=owner.get_a_chat(kwargs['identification'])) is None:
			return {'success':'False','message':'Unauthorized!','reason':'Invalid access token.'},401

		return {'success':'True','data':data_payload(requested_chat)},200