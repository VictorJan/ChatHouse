from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from chathouse.rest.tokens.verification.controller.post.template import create_a_template
from chathouse.utilities.service.mail import MailService
from chathouse.utilities.security.token import Token
from chathouse.service import UserService
from flask import current_app
from datetime import datetime

class PostVerificationStrategy(Strategy):
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

	@authorized(token_type='preaccess',location='Cookie')
	def accept(self,headers,data,**kwargs):
		'''
		Goal : Mail verification_token to an email , based on the provided <identification_data> - thus allowing a user to proceed to verify themselves.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

			headers : meant to contain all headers data , in this particular case - a cookie field as a sign of authority, must contain a preaccess_token = {route:["signup"/"login"],token_type:"preaccess",dnt}.
			Note:
				This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
				To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.
			
			data : meant to store any data that's passed into the request - json body. The could be 2 cases:
		  		signup:<identification_data>:{email:str,username:str,name:str,about:str}
		   		or
		  		login:<identification_data>={identification:str}
		  	Note:
		  		This argument is used in the verification process of the incoming request data, which is handled by the derived class template - which on itself is a result of create_a_template function, meant to return a proper template instance according to the route.
		  		To know more about the create_a_template - view a separate documentation for the create_a_template function in the ./template.py.
			
			kwargs: meant to store any data passed into the accept method, from the initial requrest, up to the authorization steps. In particular stores the authorization key , which on it's own stores shall store more nested information related to a token_type.
			In this instance the token_type is the preaccess one - so kwargs shall store:{
				authorization:{
					preaccess:{
						valid:bool,
						status:int,
						token:{
							object:None|Token,
							location:str
						}
					}
				}
			}


	 	Full verification:
	 		0.Verify the preaccess_token;
	 			If invalid respond with 401;
	  			Otherwise resume with the next steps.
  			1.Extract the route value from the token and create a proper template.
  			2.Validate the data against the proper template.
  			3.Resolve the user's email and activity using the resolve function, which returns a : dictionary of {'email':str,'activity':int} | None , based on the route and identification data.
  			If the email has been resolved :
	  			Proceed to send the email and respond accordingly with 201.
	  		Otherwise:
				Respond accordingly with 400.
	   
	   	Lambda functions:
	   		[Note each lambda function shall be called from bottom up.]s

			find_case:

				Goal: return the very first case of existing UserService from the submited search cases.
				Arguments: cases:map of cases:UserService|None.
				Returns: very first UserService instance.
				[Note at this point there must be a UserService instance, with the help of explicit validation with any(). But if there isn't one - error will not arise due to the tuple verification]

	   		map_cases: 

	   			Goal:create a map object of iterated UserService instances for email and username cases. Iteration itself checks if the instance has an id -> returns the UserService if instance has an id else None.
	   			Arguments: data:key word argument.
	   			Returns: map object.

	   		resolve:

	   			Goal: resolve email based on the identification data , by verify if the such data is appropriate according to a certain route.
	   			If the route is signup:
	   				Get respective map_cases, then :
	   					If not even one case (not any function) is valid return:
	   						{'email':as email from the provided data, 'activity': as 0}
	   					Otherwise return None
				Otherwise:
					Get respective map_cases, then convert cases into a tuple:
						If there is a case, which isn't None - then return the very next element of the filtered cases , where every case must not be a None - thus returning:
							{'email':resolved user's email, 'activity':current activity_dnt state of the resolved user}.
						Otherwise return None.
				Returns: {email:str,activir:int}|None.    

		Generation:
	  		verification_token={identification_data:<identification_data>,token_type:"verification", activity:<current_activity_dnt_state>, dnt,preaccess:<preaccess_token>}.

	 	Returns:
	 		If verified: 201,{success:True,email_sent:True}
	  		Otherwise:
	   			Failed to verify the token: 401,{success:False,message:"Unauthorized."}
	   			Failed to validate the json body: 400,{success:False,message:"Incorrect json data."}
		'''
	#Code
		#Exceptions
		assert all(map(lambda argument:isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')

		#Lambda functions

		find_case = lambda cases: next(iter(tupled)) if (tupled:=(tuple(filter(lambda case:case is not None ,cases)))) else None

		map_cases = lambda **credentials: map(lambda identification: case if (case:=UserService(**{identification:credentials[identification]})).id else None,credentials)

		resolve = lambda route,data: ( {'email':data['email'],'activity':0} if not any(map_cases(email=data['email'],username=data['username'])) else None ) if route=='signup' \
	else ({'email':case.email, 'activity': case.activity_state } if any( (cases:=tuple( map_cases(email=data['identification'],username=data['identification']) ) ) ) and (case:=find_case(cases)) else None)

		
		#Step 0.
		if not kwargs['authorization']['preaccess']['valid']:
			return {'success':'False','message':'Unauthorized!','reason':'Invalid preaccess token.'},401
		
		#Step 1.
		template = create_a_template(route:=kwargs['authorization']['preaccess']['token']['object']['route'])
		
		#Step 2.
		#Step 3.
		if template.validate(**data) and (resolution:=resolve(route,(data:=template.data))) is not None:

			verification_token=Token(payload_data={
				'identification_data':data,
				'token_type':'verification',
				'activity':resolution['activity'],
				'preaccess':kwargs['authorization']['preaccess']['token']['object'].value,
				'exp':current_app.config['VERIFICATION_EXP']
				})

			MailService.send(recipients=[resolution['email']],body=f"There has been a request to {route}, using this email. If you wish to proceed with the verification , follow this url http://127.0.0.1:5000/verify/{verification_token.value} .\nOtherwise please ignore this email.",subject="Verification email.")

			return {'success':'True','message':'Email has been sent.'},201
		else:
			return {'success':'False','message':'Data is invalid.'},400