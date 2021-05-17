from chathouse.utilities.security.controller_strategy.strategy import Strategy
from chathouse.utilities.security.validation.headers import authorized
from chathouse.rest.tokens.grant.controller.post.template import create_a_template
from chathouse.utilities.security.token import Token
from chathouse.service import UserService,KeyringService
from flask import current_app

class PostGrantStrategy(Strategy):
	'''
	PostGrantStrategy - a class, meant to be used to perform the required actions according to the defined strategy in the accept method.

	Inherits: Strategy class.
	
	Methods:
		accept - meant to perform the acceptance of the request headers and data (initated in the PostGrantController.handle(some headers,some data)),
		Core action:
			validation:
				headers with the help of authorized decorator; data with the help of certain GrantTemplate. 
			response:
				based on the validation come up with a respected response.
	'''

	@authorized(token_type='verification',location='Authorization')
	def accept(self,headers,data,**kwargs):
		'''
		Goal : Generate a grant token, based on the <identification_data> from the verification_token and the <authentication_data> from the data of the request.

		Arguments:headers:dict, data:dict, kwargs:key-word-argument.

			headers : meant to contain all headers data , in this particular case - an Authorization field as a sign of authority, must contain a Bearer token , which is the verification_token:
				{identification_data:<identification_data>,token_type:"verification",dnt,preaccess:<preaccess_token>}.
			Note:
				This argument is used in the authorized decorator - to perform proper authorization process, the result of which is stored in the kwargs.
				To know more about the authorized decorator - view a separate documentation for the authorized method in the chathouse/utilities/security/validation/headers.py.
			
			data : meant to store any data that's passed into the request - json body. The could be 2 cases:
		  		signup:
		  			<authentication_data>:{
				  		password:str,
				  		keyring:{
				  			public_key:str,
							private_key:{
								iv:str,
								data:str
							},
							g:int,
							m:int
							}
						}
		   		or
		  		login:
		  			<authentication_data>:{
				  		password:str
				  	}
		  	Note:
		  		This argument is used in the verification process of the incoming request data, which is handled by the derived class template - which on itself is a result of create_a_template function, meant to return a proper template instance according to the route.
		  		To know more about the create_a_template - view a separate documentation for the create_a_template function in the ./template.py.
			
			kwargs: meant to store any data passed into the accept method, from the initial requrest, up to the authorization steps. In particular stores the authorization key , which on it's own stores shall store more nested information related to a token_type.
			In this instance the token_type is the preaccess one - so kwargs shall store:{
				authorization:{
					verification:{
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
	  		0.Verify the verification_token:
  			1.Extract the preaccess token from the verification_token and verify it and check existance of the route value.
  				If 0./1. is invalid respond with 401, message:"Invalid verification/preaccess token.";
	  			Otherwise resume with the next steps.
  			2.Having validated the preaccess , extract the route value and create a proper template.
  			3.Verify that the data is a dictionary an proceed to validate the data against the proper template.
  			4.Resolove the appropriate user_service object (/w existing or non existing inner instance of the user) , using the resolve function , which returns a UserService|None, based on the route and <identification_data> 
  			
  			4.If the user_service has been resolved:
  				Then according to the route:
  			5.
  				If route is signup:
  			5.S.1.
  					If either provided Diffie Hellman parameters or public key is invalid:
						Respond with a 409, 'Invalid Diffie Hellman data.'
					Otherwise proceed to the next step:
			5.S.2.
  					Establish a payload using the proper_payload function and If user_service.signup(payload) has been successful:
  						Generate a grant_token and the response shall contain it with a 201.
  					Otherwise:
  						Respond with 409, 'Provided data is invalid.' if the prodived public_key doesn't already exists otherwise 'Please submit again.'
  			5.L.1.
  				Otherwise if the route is login and user_service.login( established payload) has been successful:
  					Generate a grant_token, retrieve a private key from the keyring and DH parameters => inject them into the response, and respond with a 200.
  					At this point the token_version has been incremented to avoid the usage of previously generated valid tokens.
  				Otherwise:
  					Respond with 401, message:"Invalid authentication data".
  			Otherwise:
  				Respond accordingly with 400, 'Invalid payload data'
	   
	   	Lambda functions:
	   		map_cases: 
	   			Goal:create a map object of iterated UserService instances for email and username cases. Iteration itself checks if the isntance has an id -> returns the UserService case if instance has an id else None.
	   			Arguments: data:key word argument.
	   			Returns: map object.

	   		resolve:
	   			Goal: resolve email based on the identification data , by verify if the such data is appropriate according to a certain route.
	   			If the route is signup:
	   				Get respected map_cases, then :
	   					If not even one case (not any function) is valid return then return a UserService instance with empty inner instance of the user.
	   					Otherwise return None
				Otherwise:
					Get respected map_cases, then convert cases into a tuple:
						If any case isn't None - then return next element of the filtered cases , where every case must not be a None - thus returning an email.
						Otherwise return None.
				Returns: str|None , str - represents an email value.

			valid_dh_parameters:
				Goal: verify if the provided dh parameters are the same as the configured ones, and the provided public is in bounds 0<public_key<modulus.
				Helps to omit requests, which contain invalid DH parameters meant for the key establishments.
				Arguments:initial_keyring:dict - the keyring from the provided data.
				Returns: True|False
				Note: When called the g,m values are popped - so, the keyring now has a following structure:
				keyring:{
					public_key:str,
					private_key:{
						iv:str,
						data:str
						}
					}


			proper_payload:
				Goal: construct a proper payload based on the incoming_route value and incoming_data.
				Arguments: incoming_route:str,incoming_data:dict.
				Actions:
					If the route is signup ( Note: at this point incoming_data consists of : password:str , keyring:{ public_key:str , private_key: { iv:str,data:str } } ):
						return {
							key_data : pop the keyring from the incoming_data
							user_data : {unpack the <identification_data> from the verification token , and unpack the incoming_data}
						}.
					Otherwise the route is login ( Note at this point incoming_data consists of : password:str ):
						return incoming_data.
				Returns: a dictionary.

		Generation:
  			grant_token={user_id: value:int, token_type: "grant":str, token_version: UserService(id=value of user_id).token_version , dnt:float}
 
		Returns:
			If either verification token or preaccess token(from the verification token) is invalid or the preaccess token has no route value.
  				Return 401, message:"Invalid verification/preaccess token."
  			Otherwise:
  				If route is signup:
  					If either provided Diffie Hellman parameters or public key is invalid:
						Respond with a 409, 'Invalid Diffie Hellman data.'
					Otherwise:
						 If the user_service.signup(appropriate payload) has been successful:
						 	Return 200, {grant_token:<grant_token>}
						 Otherwise:
						 	Return 409, 'Provided data is invalid.' if the prodived public_key doesn't already exists otherwise 'Please submit again.'
  				Otherwise if the route is login and user_service.login(appropriate payload) has been successful:
  					Return 200, {grant_token:<grant_token>,keyring:{raw:{private_key:<encrypted private_key>}, g:<G>, m:<M>}}
  				Otherwise:
  					Return 401, 'Invalid authentication data.'

  		Exceptions:
  			Raises:
  				TypeError - if headers and data arguments are not dictionaries.
  				ValueError - if the current app  doesn't contain domain Diffie Hellman parameters.
		'''
	#Code:
		#Exceptions:
		assert all(map(lambda argument: isinstance(argument,dict),(headers,data))), TypeError('Arguments , such as : headers and data - must be dictionaries')
		assert all(map(lambda parameter: isinstance(parameter,int) ,current_app.config.get('DH_PARAMETERS',(None,)))), ValueError('Configuration of the current app must contain domain Diffie Hellman parameters.')

		#Lambda functions:
		map_cases = lambda **data: map( lambda case: case if case.id is not None else None ,( UserService(email=data.get('email')) , UserService(username=data.get('username')) ) )
		
		resolve = lambda route,data: (UserService() if not any(map_cases(email=data['email'],username=data['username'])) else None ) if route=='signup'\
		else (next(filter(lambda case:case is not None ,cases))	if any( (cases:=tuple( map_cases(email=data['identification'],username=data['identification']) ) ) ) else None)

		valid_dh_parameters = lambda initial_keyring: current_app.config['DH_PARAMETERS']==(initial_keyring.pop('g',None),initial_keyring.pop('m',None)) and 0<initial_keyring['public_key']<current_app.config['DH_PARAMETERS'][1] 

		proper_payload = lambda incoming_data,incoming_route: { \
			 'key_data':incoming_data.pop('keyring'),\
			 'user_data':{**kwargs['authorization']['verification']['token']['object']['identification_data'],**incoming_data} \
			 } if incoming_route=='signup' else incoming_data


		#Step 0.
		#Step 1.
		if not kwargs['authorization']['verification']['valid'] or not (preaccess_token:=Token(raw_data=kwargs['authorization']['verification']['token']['object']['preaccess'])).is_valid or not preaccess_token['route']:
			return {'success':'False','message':'Unauthorized!','reason':'Invalid verification/preaccess token.'},401
		
		#Step 2.
		template = create_a_template(route:=preaccess_token['route'])

		#Step 3.
		#Step 4.
		if isinstance(data,dict) and template.validate(**data) and (user_service:=resolve(route,kwargs['authorization']['verification']['token']['object']['identification_data'])) is not None:
			
			data=template.data
		#Step 5.
			if route=='signup':
		#Step 5.S.1
				if not (dh_is_valid:=valid_dh_parameters(data['keyring'])):
					return {'success':'False','message':'Invalid Diffie Hellman data.'},409
		#Step 5.S.2
				if user_service.signup(**(su_payload:=proper_payload(data,route))):
				
					return {'success':'True',\
					'grant_token':Token(payload_data={'user_id':user_service.id,'token_type':'grant','token_version':user_service.token_version,'exp':{'minutes':30}}).value\
					},201

				else:

					return {'success':'False',\
					'message': ('Please submit again.' if KeyringService(public_key=su_payload['key_data']['public_key']).id else 'Provided data is invalid.') },\
					409
		#Step 5.L.1
			elif route=='login' and user_service.login(**proper_payload(data,route)):
				return {'success':'True',\
				'grant_token':Token(payload_data={'user_id':user_service.id,'token_type':'grant','token_version':user_service.token_version,'exp':{'minutes':30}}).value,\
				'keyring':{ 'raw':{'private_key':user_service.keyring.private_key}, **dict(zip('gm',current_app.config['DH_PARAMETERS'])) }
				},201
			
			else:
				return {'success':'False','message': 'Invalid authentication data!'},401

		else:
			print(template.validate(**data))
			return {'success':'False','message':'Invalid payload data.'},400