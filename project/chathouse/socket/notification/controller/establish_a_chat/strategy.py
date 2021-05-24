from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from chathouse.socket.notification.controller.establish_a_chat.template import create_a_template
from chathouse.service import UserService
from flask_socketio import emit,disconnect

class Establish_a_ChatNotificationStrategy(Strategy):
	'''
	Establish_a_ChatNotificationStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the Establish_a_ChatNotificationController.handle(some headers,some data)),
		Core action:
			validation:
				headers with the help of authorized decorator. 
				data with the help of a Template instance.
			response:
				based on the validation come up with a respected response.
	'''

	@authorized(token_type='access',location='Authorization')
	def accept(self,headers,data,**kwargs):
		'''
		Goal : establish/create a chat instance and join the chat on the behalf of the requester and the other participant, if provided.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

			headers : meant to contain all headers data , in this particular case - an Authorization field as a sign of authority, must contain a "Bearer <token> , which is the access_token:
				access_token={user_id:int, token_type: "access":str, token_version:int , dnt:float}
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
			resolve:
				Goal: resolve a UserService instance with existing inner user instance, based on the provided provided identification.
				Arguments:credentials:key-word-argument. Expecting a key/value pair such as id/<int>.
				Actions:
					If there is a UserService instance with inner existing user instance:
						Such participant exists - return ther UserService instance
					Otherwise return None
				Returns: UserService instance | None

	 	Full verification and actions:
	  		0.Verify the access_token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService, and verifies the provided token_version with the current one related to the UserService :
  				If 0. is invalid - disconnect the client.
  				[Note, on the response the user reconnects ,after they try to reestablish a new access_token]
	  			Otherwise proceed to the next steps.
	  		1.At this point the access_token is valid - validate the incoming data:
	  			Set up a template - using a custom create_template, which builds and returns a Template instance.
	  			Validate the data against the template:
	  				If the verification has been successful and:
	  					If the product of the validation / validated doesn't contain a participant_id set other_participant as None and resume the condition to end up successful. -> step 2.
	  					Otherwise If the product of the validation / validated contains a participant_id and the resolution has returned a UserService - thus has found such user - follow the next step -> step 2.
	  		2.			Owner starts a chat -> creates an instance of a ChatService , If everything has gone well:
		  	2.1				On the behalf of each "soon to be participant" - join the chat.
		  					If at any point a UserService wasn't able to join the chat:
		  						The provided payload - was invalid : the request contained the credentials of users that already were related to the chat. 
		  	2.1[-]				Discharge/Remove the created chat, and mention this to requester/owner.
		  	2.2				Otherwise proceed to the notify each participant of the chat - using the participations property.
	  		2.[-]		Otherwise:
	  							The chat couldn't be created - notify the owner of the request/access_token about the failure
	  		1.[-]		Otherwise - the resolution wasn't able to figure out the user based on the credentials proceed to the mention about the failure.
	  		1.[-]	Otherwise proceed to mention about the failure.


  		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.
		'''
	#Code:
		#Exceptions:
		assert all(map(lambda argument: isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')

		resolve = lambda **credentials:  instance if (instance:=UserService(**credentials)).id else None

		#Step 0.
		if not kwargs['authorization']['access']['valid'] or (owner:=kwargs['authorization']['access']['owner']) is None:
			disconnect()
			return None

		template = create_a_template()
		#Step 1.
		if template.validate(**data) and ( True if (other_participant:=(validated:=template.data).get('participant_id',None)) is None else (other_participant:=resolve(id=other_participant)) is not None and other_participant.id!=owner.id ):
			#Step 2.			
			if (chat:=owner.establish_a_chat(validated['name'])):
			#Step 2.1
				for instance in (owner,* ( (other_participant,) if other_participant else ()) ):
			#Step 2.1[-]
					if not (result:=instance.join_a_chat(chat.id)):
						
						owner.discharge_a_chat(chat.id)

						emit('error',{'message':'Invalid payload.It seems the user is already related to the chat.'},to=owner.id)
						
						return None

			#Step 2.2
				for participant in chat.participants:
					emit('established_chat',{'id':chat.id,'name':chat.name},to=participant.id)
			
			#Step 2.[-]
			else:
				emit('error',{'message':'Invalid payload.The chat couldn\'t be established.'},to=owner.id)

		#Step 1.[-]
		else:
			emit('error',{'message':'Invalid payload.'},to=owner.id)

		return None