from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from chathouse.rest.users.identified.controller.put.template import create_a_template
from flask import current_app

class PutIdentifiedUserStrategy(Strategy):
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
		Goal : Change/reset a password of a requested user, having provided a respective authority - confirmation token , ownership of which references the requested user.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

		headers : meant to contain all headers data , in this particular case - an Authorization field as a sign of authority, must contain a "Bearer <token> , which is the confirmation_token:
			confirmation_token={user_id:int, action:str("put"|"delete") token_type:str("confirmation"), activity:int , dnt:float}
		Note:
			This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
			To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.

		data : meant to store any data that's passed into the request - json body:
		{
			password:{
				current:str (already hashed),
				new:str (already hashed)
			},
			private_key:{iv:str,data:str}
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
	  		0.Verify the confirmation_token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService, and verifies the provided activity with the current one related to the UserService :
  			1.Make sure that the requester's/owner's id is the same as the provided identification and the action value of the confirmation tokes is put , also.
  				If 0.|1. is invalid respond with 401, message:"Invalid confirmation token.";
	  			Otherwise head to the following steps.
	  		2.Create a proper data template.
	  		3.Validate incoming data againt the template.
	  		If the execution has been successful , proceed to reset the password.
	  			If the reset proceedure has been victorious:
	  				The password has been reset, the private_key has been changed  and the activity state has been updated.
	  				Respond with 200, notifying about the fortunate reset.
	  			Otherwise:
	  				Respond with 400, mentioning about the incorrect authentication data.
	  		Othewise:
	  			Respond with 400, stating about the invalid payload.
	  		
 
		Returns:
			If the confirmation_token(the ownership,signature) is invalid or the owner's id is not equal to the one provided in the URL or the action value in the confirmation token in innapropriate:
  				Return 401, message:"Unauthorized!","reason":"Invalid confirmation token."
  			Otherwise:
  				If the provided data is valid:
					If the current password has matched the one in the database, the password has been reset -> thus the private_key too and activity state has been updated:
						Return 200,message:"The password has been reset and the activity has been updated, please proceed to login using new credentials."
					Otherwise:
						Return 401, message:"Unauthorized!", reason:"Invalid authentication data".
  				Othewise:
  					Return 400,  message:"Bad request!",reason:"Invalid payload."

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
		if not kwargs['authorization']['confirmation']['valid'] or kwargs['authorization']['confirmation']['token']['object']['action']!="put" or (owner:=kwargs['authorization']['confirmation']['owner']) is None or owner.id!=kwargs['identification']:
			return {'success':'False','message':'Unauthorized!','reason':'Invalid confirmation token.'},401

		template=create_a_template()

		if template.validate(**data):
			
			data=template.data

			if owner.reset_password(**data['reset']):
				return {'success':'True','message':'The password has been reset and the activity has been updated, please proceed to login using new credentials.'},200	
			else:
				return {'success':'False','message':'Unauthorized!','reason':'Invalid authentication data.'},401
		else:
			return {'success':'False','message':'Bad request!','reason':'Invalid payload.'},400