from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from chathouse.rest.users.identified.controller.delete.template import create_a_template
from flask import current_app

class DeleteIdentifiedUserStrategy(Strategy):
	'''
	PutIdentifiedUserStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the PutIdentifiedUserController.handle(some headers,some data)),
		Core action:
			validation:
				headers with the help of authorized decorator. 
			response:
				based on the validation come up with a respective response.
	'''

	@authorized(token_type='confirmation',location='Authorization')
	def accept(self,headers,data,**kwargs):
		'''
		Goal : Delete entitiy of a requested user, having provided a respective authority - confirmation token , ownership of which references the requested user.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

		headers : meant to contain all headers data , in this particular case - an Authorization field as a sign of authority, must contain a "Bearer <token> , which is the confirmation_token:
			confirmation_token={user_id:int, token_type: "confirmation":str, activity:int , dnt:float}
		Note:
			This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
			To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.

		data : meant to store any data that's passed into the request - in this case:
		{
			password:str
		}
			
		kwargs: meant to store any data passed into the accept method, from the initial requrest, up to the authorization steps. In particular stores :
		The identification at : { identification:int }
		In this instance the token_type is the confirmation one - so kwargs shall store:{
			authorization:{
				confirmation:{
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
	  		0.Verify the confirmation_token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService, and verifies the provided token_version with the current one related to the UserService :
  			1.Make sure that the requester's/owner's id is the same as the provided identification and the action value of the confirmation token is delete , also.
  				If 0.|1. is invalid respond with 401, message:"Invalid confirmation token.";
	  			Otherwise head to the following steps.
	  		2.Execute the validation of the incoming data , with the help of a properly created template.
	  		If the incoming data has been proven to be valid:
	  			3.Terminate the requested user's / owner's entity, providing the password from the validated data.
	  			If the discharing has been successful, respond with 200,message:"The account has been successfuly discharged.".
	  			Otherwise, respond with 401 , message:"Invalid authentication data."
	  		Otherwise, respond with 400, message:"Bad request!", reason:"Invalid payload."
 
		Returns:
			If the confirmation_token(the ownership,signature) is invalid or the owner's id is not equal to the one provided in the URL, or the action value in the confirmation token in innapropriate:
  				Return 401, message:"Unauthorized!","reason":"Invalid confirmation token."
  			Otherwise:
  				If the provided request data is valid according to the template:
  					If user's instance has been fortunately discharged:
  						Returns 200, informing about the successful outcome of the removal process.
  					Otherwise - the password could have been invalid, notify the requester, returning 401, reason:"Invalid authentication data."
  				Othewise - the incoming request data has been determined to be invalid - return a 400, reason:"Invalid payload."

  		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.
  				TyperError - if the identification argument is not provided or the datatype of the value is not an integer.
		'''
	#Code:
		#Exceptions:
		assert all(map(lambda argument: isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')
		assert isinstance(kwargs.get('identification',None),int), TypeError('The identification argument hasn\'t been submited or the data type is invalid.')
		
		#Step 0.
		#Step 1.
		if not kwargs['authorization']['confirmation']['valid'] or kwargs['authorization']['confirmation']['token']['object']['action']!="delete" or (owner:=kwargs['authorization']['confirmation']['owner']) is None or owner.id!=kwargs['identification']:
			return {'success':'False','message':'Unauthorized!','reason':'Invalid confirmation token.'},401
		
		#Step 2.
		template=create_a_template()
		if template.validate(**data):
			#Step 3.
			return ({'success':'True','message':'The account has been successfuly discharged.'},200) if owner.remove(**template.data) else ({'success':'False','message':'Unauthorized!','reason':'Invalid authentication data.'},401)
		return {'success':'False','message':'Bad request!','reason':'Invalid payload.'},400