from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized

class GetUsersStrategy(Strategy):
	'''
	GetUsersStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the GetUsersController.handle(some headers,some data)),
		Core action:
			validation:
				headers with the help of authorized decorator. 
			response:
				based on the validation come up with a respective response.
	'''

	@authorized(token_type='access',location='Authorization')
	def accept(self,headers,data,**kwargs):
		'''
		Goal : Retreive some unique data about each found user, based on the provided identification.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

		headers : meant to contain all headers data , in this particular case - an Authorization field as a sign of authority, must contain a "Bearer <token> , which is the access_token:
			access_token={user_id:int, token_type: "access":str, activity:int , dnt:float}
		Note:
			This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
			To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.

		data : meant to store any data that's passed into the request - in this case, data is irrelevant:
			
		kwargs: meant to store any data passed into the accept method, from the initial requrest, up to the authorization steps. In particular stores :
		The identification at : { identification:str }
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
			user_payload:
				Goal: return a dictionary containing some unique information about the user.
				Arguments: user:UserService. 
				Returns: dict('id':<id>,'username':<username>)

			users_payload:
				Goal: return a list of found users, which contains unique data from the user_payload.
				Arguments: users:tuple(of UserServices, with ids of queried/enquired users | empty). 
				Returns: list(for each user <user_payload(user):dict>,...)

			data_payload:
				Goal: structure and return a list meant for the data key in the response.
				Arguments: requester:UserService
				Returns: a list of ( dictionaries for each user (id:<user.id:int>,username:<user.username:str>) | empty if the query couldn't resolve any users)

	 	Full verification:
	  		0.Verify the access_token , which on it's own - verifies ownership - makes sure of the existance of a user with the user_id - establishing a UserService, and verifies the provided activity with the current one related to the UserService :
  				If 0. is invalid respond with 401, reason:"Invalid access token.";
				Otherwise proceed to the next step.
			1.Verify that the identification filter is present
				If 1. is invalid respond with 400, reason:"IThe identification filter is not provided.";
	  			Otherwise head to the generation phase.
	  		
		Generation:
  			data=[{
					id:<user's id:int>
					username:<user's username:str>
				},...]
	  		}
 
		Returns:
			If the access_token(the ownership,signature) is invalid:
  				Return 401, message:"Unauthorized!","reason":"Invalid access token."
  			Otherwise if there GET parameter for the identification hasn't been provided or is empty:
  				Return 400, message:"Bad Request!","reason":"The identification filter is not provided."
  			Otherwise:
  				Return 200, data:<users_data>

  		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.
		'''
	#Code:
		#Exceptions:
		assert all(map(lambda argument: isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')
		

		#Lambda functions:

		user_payload = lambda user: {'id':user.id,'username':user.username}

		users_payload = lambda users: [ user_payload(user) for user in users ] if users else []
		
		data_payload = lambda requester: users_payload(requester.get(name=kwargs['identification'],username=kwargs['identification']))

		#Step 0.
		if not kwargs['authorization']['access']['valid'] or (owner:=kwargs['authorization']['access']['owner']) is None:
			return {'success':'False','message':'Unauthorized!','reason':'Invalid access token.'},401
		#Step 1.
		if not kwargs['identification']:
			return {'success':'False','message':'Bad request!','reason':'The identification filter is not provided.'},400

		return {'success':'True','data':data_payload(owner)},200