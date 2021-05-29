from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from chathouse.socket.chat.controller.establish_a_message.template import create_a_template
from chathouse.service import UserService
from flask_socketio import emit,disconnect
from datetime import datetime

class Establish_a_MessageChatStrategy(Strategy):
	'''
	Establish_a_MessageChatStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the Establish_a_MessageChatController.handle(some headers,some data)),
		Core action:
			validation:
				headers with the help of authorized decorator. 
				data with the help of a Template instance.
			response:
				based on the validation come up with a respective response.
	'''

	@authorized(token_type='access',location='Authorization')
	def accept(self,headers,data,**kwargs):
		'''
		Goal : establish/create a new message instance in a provided chat.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

			headers : meant to contain all headers data , in this particular case - an Authorization field as a sign of authority, must contain a "Bearer <token> , which is the access_token:
				access_token={user_id:int, token_type: "access":str, activity:int , dnt:float}
			Note:
				This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
				To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.
			
			data : meant to store any data that's passed into the request - json body, there could 2 cases:
		  		With another participant:
		  		{
					name:str,
					participnat_id:<int>
		  		}
		   		or without one:
		  		{
		  			name:str
		  		}
		  	Note:
		  		This argument is used in the verification process of the incoming request data, which is handled by the derived class template - which on itself is a result of create_a_template function, meant to return a proper template instance according to the route.
		  		To know more about the create_a_template - view a separate documentation for the create_a_template function in the ./template.py.
		  	
			kwargs: meant to store any data passed into the accept method, from the initial requrest, up to the authorization steps. In particular stores the authorization key , which on it's own stores shall store more nested information related to a token_type.
			The chat identification : chat_id:int.
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
			sender_payload:
				Goal: return a dictionary containing some unique information about the sender of the message.
				Arguments: sender:UserService. 
				Returns: dict('id':<id>,'username':<username>)

			message_payload:
				Goal: return a dictionary containing information about a message.
				Arguments: message:MessageService. 
				Returns: dict(id:<message id:int>,content:dict(iv:str,data:str),dnt:dict(timestamp:int,readable:str),sender:sender_payload(<message.sender>))

			activity_payload:
				Goal: return a dictionary containing information about a chat , which has been affected with the establishment.
				Arguments: chat:ChatService. 
				Returns: dict(id:<chat id:int>, name<chat's name:str>)

	 	Full verification and actions:
	  		0.Verify the access_token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService, and verifies the provided activity with the current one related to the UserService :
  				1.Make sure that the provided chat identification is an integer and that the owner is a participant of a chat with such identification - extracting a ChatService instance.
  				If 0.|1. is invalid - disconnect the client.
  				[Note, on the response the user reconnects ,after they try to reestablish a new access_token]
	  			Otherwise proceed to the next steps.
	  		2.At this point the access_token is valid - validate the incoming data:
	  			Set up a template - using a custom create_template, which builds and returns a Template instance.
	  			Validate the data against the template:
	  				If the verification has been successful:
	  		3.     		Establish/create a message , providing the chat identification and the provided encrypted content.
	  					If the establishment has been successful:
	  		3.1				First and foremost notify each participant in the room/ the room with the <message paylod>
	  		3.2				Then notify each participant, whose not even in the room, about the activity , by emiting to a <notification payload> to assinged rooms.
	  		3.[-]		Otherwise:
	  						The message couldn't be created - notify the owner of the request/access_token about the failure.
	  		2.[-]	Otherwise - the provided data payload wasn\'t valid, according to the custom template.
	  		
		
		Generation:
			message payload:
				{
					id:<message id:int>
					content:{ iv:<iv:str> , data:<data:str> },
					sender:{id:<sender's id:int>, username:<sender's username:str>}
					dnt: { timestamp:<timestamp value:int>, readable:<visually comprehensible:str> }
				}

  		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.

  		Returns: None
		'''
	#Code:
		#Exceptions:
		assert all(map(lambda argument: isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')

		sender_payload = lambda sender: {'id':sender.id,'username':sender.username}

		message_payload = lambda message: {'id':message.id, 'content':message.content, 'dnt':{'timestamp':int(datetime.timestamp(message.dnt)), 'readable':str(message.dnt.time()) }, 'sender':sender_payload(message.sender)}

		activity_payload = lambda chat: {'id':chat.id, 'name':chat.name}
		

		#Step 0.
		#Step 1.
		if not kwargs['authorization']['access']['valid'] or (owner:=kwargs['authorization']['access']['owner']) is None or not isinstance(kwargs['chat_id'],int) or (chat:=owner.get_a_chat(kwargs['chat_id'])) is None:
			disconnect()
			return None

		template = create_a_template()
		#Step 2.
		if template.validate(**data):
			
			data=template.data
			
			#Step 3.
			if (message:=owner.establish_a_message(chat_id=chat.id,content=data['content'])):

				#Step 3.1.
				emit('established_message',message_payload(message),to=chat.id)

				#Step 3.2.
				for participant in chat.participants:
					emit('chat_activity',activity_payload(chat),namespace='/socket/notification',to=participant.id)
			
			#Step 3.[-]
			else:
				emit('error',{'message':'The message couldn\'t be established, please try again.'},namespace='/socket/notification',to=owner.id)
			
		#Step 2.[-]
		else:
			emit('error',{'message':'Please submit a valid payload.'},namespace='/socket/notification',to=owner.id)
		
		return None