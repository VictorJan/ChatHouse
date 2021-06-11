from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from chathouse.socket.notification.controller.discharge_a_chat.template import create_a_template
from chathouse.service import UserService
from flask_socketio import emit,disconnect
from flask import request

class Discharge_a_ChatNotificationStrategy(Strategy):
	'''
	Discharge_a_ChatNotificationStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the Discharge_a_ChatNotificationController.handle(some headers,some data)),
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
		Goal : as a participant of a chat - discharge/remove/delete the provided chat - thus clearing all of the related messages and participations.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

			headers : meant to contain all headers data , in this particular case - an Authorization field as a sign of authority, must contain a "Bearer <token> , which is the access_token:
				access_token={user_id:int, token_type: "access":str, activity:int , dnt:float}
			Note:
				This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
				To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.
			
			data : meant to store any data that's passed into the request - json body:
		  		{
					id:<int>
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

	 	Full verification and actions:
	  		0.Verify the access_token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService, and verifies the provided activity with the current one related to the UserService :
  				If 0. is invalid - disconnect the client.
  				[Note, on the response the user reconnects ,after they try to reestablish a new access_token]
	  			Otherwise proceed to the next steps.
	  		1.At this point the access_token is valid - validate the incoming data:
	  			Set up a template - using a custom create_template, which builds and returns a Template instance.
	  			Validate the data against the template:
	  				If the verification has been successful and:
	  					The product of the validation / validated shall contain an "id" which refers to an ID of a chat , of which the owner ,of the request/access token, must be a participant!
	  		2.			Therefore verify if the owner is a participant of the provided chat:
	  						Then perform the discharging/removing/trashing the chat.
	  		2.1				If everything has been successful:
	  							Having previously stored the participants of the removed chat, notify each each of them , with a proper notification on "discharged_chat" event.
	  		2.1[-]			Otherwise there has been a confilct inside of the database inform the requester to try again.
	  		2.[-]		Otherwise:
							Notify with a message implying about the unauthorized access.
	  		1.[-]		Otherwise - the resolution wasn't able to figure out the user based on the credentials proceed to the mention about the failure.
	  		1.[-]	Otherwise proceed to mention about the failure.


  		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.
		'''
	#Code:
		#Exceptions:
		assert all(map(lambda argument: isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')

		#Step 0.
		if not kwargs['authorization']['access']['valid'] or (owner:=kwargs['authorization']['access']['owner']) is None:
			disconnect()
			return None

		template = create_a_template()
		#Step 1.
		if template.validate(**data):
			
			validated=template.data

			#step 2.
			if (chat:=owner.get_a_chat(validated['id'])):
				participants=tuple(participant.id for participant in chat.participants)
				#Step 2.1.
				if owner.discharge_a_chat(chat.id):
					for participant in participants:
						emit('discharged_chat',{'id':validated['id']},to=participant)
				else:
					emit('error',{'message':'Please try again.'})
			
			#Step 2.[-]
			else:
				emit('error',{'message':'Unauthorized actions.Must be a participant of the provided chat.'})
		
		#Step 1.[-]
		else:
			emit('error',{'message':'Invalid payload.'},to=owner.id)

		return None