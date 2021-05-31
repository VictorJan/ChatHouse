from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from chathouse.rest.tokens.confirmation.controller.post.template import create_a_template
from chathouse.utilities.service.mail import MailService
from chathouse.utilities.security.token import Token
from flask import current_app
from datetime import datetime

class PostConfirmationStrategy(Strategy):
	'''
	PostVerificationStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the PostVerificationController.handle(some headers,some data)),
		Core action:
			validation:
				headers with the help of authorized decorator; data with the help of certain VerificationTemplate. 
			response:
				based on the validation come up with a respective response.
	'''

	@authorized(token_type='access',location='Authorization')
	def accept(self,headers,data,**kwargs):
		'''
		Goal : Mail verification_token to an email , based on the provided <identification_data> - thus allowing a user to proceed to verify themselves.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

			headers : meant to contain all headers data , in this particular case - a cookie field as a sign of authority, must contain a preaccess_token = {route:["signup"/"login"],token_type:"preaccess",dnt}.
			Note:
				This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
				To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.
			
			data : meant to store any data that's passed into the request - json body:
		  		action:str(delete|put)

		  	Note:
		  		This argument is used in the verification process of the incoming request data, which is handled by the derived class template - which on itself is a result of create_a_template function, meant to return a proper template instance according to the route.
		  		To know more about the create_a_template - view a separate documentation for the create_a_template function in the ./template.py.
			
			kwargs: meant to store any data passed into the accept method, from the initial requrest, up to the authorization steps. In particular stores the authorization key , which on it's own stores shall store more nested information related to a token_type.
			In this instance the token_type is the preaccess one - so kwargs shall store:{
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
	 		0.Verify the access_token;
	 			If invalid respond with 401;
	  			Otherwise resume with the next steps.
  			1.Create a proper template for validating provided data.
  			2.Validate the data against the proper template.
  			3.If validation has been successful -> update the current activity state of the requester/owner of the access token.
  			[-]If either 2.|3. has been unsuccessful - respond with 400
  			[+]Otherwise proceed to the generate a confirmation token and send it to the requester/access token owner as an email. Responding with 201 and a proper message.
  			
  		Generation:
	  		confirmation_token={user_id:int(request's/owner's id), action:str(requested action),token_type:str("confirmation"), activity:int(current user's activity state), dnt:float }.

	 	Returns:
	 		If verified: 201,{success:True,email_sent:True}
	  		Otherwise:
	   			Failed to verify the token: 401,{success:False,message:"Unauthorized."}
	   			Failed to validate the json body: 400,{success:False,message:"Incorrect json data."}
		'''
	#Code
		#Exceptions
		assert all(map(lambda argument:isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')

		#Step 0.
		if not kwargs['authorization']['access']['valid'] or (owner:=kwargs['authorization']['access']['owner']) is None:
			return {'success':'False','message':'Unauthorized!','reason':'Invalid access_token'},401
		
		#Step 1.
		template = create_a_template()
		
		#Step 2.
		#Step 3.
		if template.validate(**data) and owner.update_activity():
			
			data=template.data

			confirmation_token=Token(payload_data={
				'user_id':owner.id,
				'action':data['action'],
				'token_type':'confirmation',
				'activity':owner.activity_state,
				'exp':current_app.config['CONFIRMATION_EXP']
				})

			MailService.send(recipients=[owner.email],body=f"Greetings, {owner.username}!\nThere has been a request to {'reset' if data['action']=='put' else data['action']} your data. If you wish to proceed with the confirmation , follow this url http://127.0.0.1:5000/confirm/{confirmation_token.value} .\nOtherwise please ignore this email.",subject="Confirmation email.")

			return {'success':'True','message':'Confirmation email has been sent.'},201
		else:
			return {'success':'False','message':'Data is invalid.'},400