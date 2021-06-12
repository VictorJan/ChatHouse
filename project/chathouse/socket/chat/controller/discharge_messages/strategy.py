from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from chathouse.socket.chat.controller.discharge_messages.template import create_a_template
from flask_socketio import emit,disconnect

class Discharge_MessagesChatStrategy(Strategy):
	'''
	Discharge_a_MessageChatStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the Discharge_a_MessageChatController.handle(some headers,some data)),
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
		Goal : as a participant of a provided chat - remove/delete/discharge any provided messages, that are contained in the chat.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

			headers : meant to contain all headers data , in this particular case - an Authorization field as a sign of authority, must contain a "Bearer <token> , which is the access_token:
				access_token={user_id:int, token_type: "access":str, activity:int , dnt:float}
			Note:
				This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
				To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.
			
			data : meant to store any data that's passed into the request - json body:
		  		{
					messages:list(of <int>s)
		  		}

		  	Note:
		  		This argument is used in the verification process of the incoming request data, which is handled by the derived class template - which on itself is a result of create_a_template function, meant to return a proper template instance according to the route.
		  		To know more about the create_a_template - view a separate documentation for the create_a_template function in the ./template.py.
		  	
			kwargs: meant to store any data passed into the accept method, from the initial requrest, up to the authorization steps. In particular stores the authorization key , which on it's own stores shall store more nested information related to a token_type.
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

		lambda functions:

			discharged_payload:
				Goal: return a dictionary containing a list of the terminated/deleted messages.
				Arguments: messages:list. 
				Returns: dict(messages:<messages:list>)

			activity_payload:
				Goal: return a dictionary containing information about a chat , which has been affected with the establishment.
				Arguments: chat:ChatService. 
				Returns: dict(id:<chat id:int>, name<chat's name:str>)

			discharges:
				Goal: set a generator of successfully discharged messages.
				Arguments: service:UserService, chat_identification:int, identifications:list of int_s
				Actions:
					Iterate through the messsage identifications , and for each of them execute a method to remove the message, providing the chat identification and the respective message id.
					If the discharge has been successful - return the identification of the removed message.
				Returns: generator


	 	Full verification and actions:
	  		0.Verify the access_token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService, and verifies the provided activity with the current one related to the UserService :
  				1.Make sure that the provided chat identification is an integer and that the owner is a participant of a chat with such identification - extracting a ChatService instance.
  				If 0.|1. is invalid - disconnect the client.
  				[Note, on the response the user reconnects ,after they try to reestablish a new access_token]
	  		2.At this point the access_token is valid - validate the incoming data:
	  			Set up a template - using a custom create_template, which builds and returns a Template instance.
	  			Validate the data against the template:
	  				If the verification has been successful and:
	  					The product of the validation / validated shall contain a list of messages - which consist of message ids ,that shall be contained in the / related to the provided chat!
	  		3.			Therefore proceed to remove each message:
	  					Iterate through each message , executing a discharge for each message -> which shall store the message_id's of the messages that have been discharged.
						Having iterated the generator - we shall store the result as "discharged" list of messages , then if the outcome doens't correspond to the incomming messages:
							Notify the requester about the invalid payload.
			4.1			Then if there are any discharged messages - notify the current participants of the chat / the chat about the removed messages, with a proper notification on "discharged_messages".
			4.2			Apart from that, make sure to declare about the activity to all participants, using the notification namespace and appropriate rooms.	
			
	  		2.[-]	Otherwise proceed to mention about the failure.


  		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.
		'''
	#Code:
		#Exceptions:
		assert all(map(lambda argument: isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')

		#Lambda functions:
		discharged_payload = lambda messages: {'messages':messages}
		activity_payload = lambda chat: {'id':chat.id, 'name':chat.name}
		discharges = lambda service,chat_identification,identifications: (identification for identification in identifications if service.discharge_a_message(chat_id=chat_identification,message_id=identification))

		#Step 0.
		#Step 1.
		if not kwargs['authorization']['access']['valid'] or (owner:=kwargs['authorization']['access']['owner']) is None or not isinstance(kwargs['chat_id'],int) or (chat:=owner.get_a_chat(kwargs['chat_id'])) is None:
			disconnect()
			return None
		
		template = create_a_template()
		#Step 2.
		if template.validate(**data):
			
			validated=template.data
			#Step 3.
			if (discharged:=list(discharges(owner,chat.id,validated['messages'])))!=validated['messages']:
				emit('error',{'message':"Invalid payload - not all provided messages have been discharged."}, namespace='/socket/notification', to=owner.id)

			#Step 4.
			if discharged:
				#Step 4.1
				emit('discharged_messages',discharged_payload(discharged),to=chat.id)
				#Step 4.2
				for participant in chat.participants:
					emit('chat_activity', activity_payload(chat),namespace='/socket/notification',to=participant.id)
		#Step 2.[-]
		else:
			emit('error',{'message':'Invalid payload.'},namespace='/socket/notification',to=owner.id)

		return None