from chathouse.utilities.security.token import Token
from chathouse.service import UserService,ChatService
from functools import wraps
import re

def authorized(token_type,location=None):
	'''
	Goal:Validate authorization, relying on the JWT tokens, that could be passed to <location>=[Cookie/Authorization/<other>/None] and <token_type>=[preaccess/verification/grant/access].
 	Verify the signature, token_type - for certain tokens take into consideration : ownership and token_version.

 	Chained Authorization:
 		The decorater shall accept other authorization keys, present in the Key word argument, and move along with them, only IF:
			Each <token_type> is unique , creating the following structure:
			'authorization':{
				<token_type1>:{
					valid:<True/False>,
					status_code:<200/401>,
					token:<{
						location:<location/None>,
						object:<Token/None>
					}>
				}
				<token_type2>:{...}
			}
			Thus, for each call, each block has to be independently validated for any exceptions.
			Permitted chaining of the "authorized" decorators:
			[token_type1=type1,location=location1]~>[token_type1=type2,location=location1]~>[token_type1=type6,location=location2]

 	Arguments: location=[Cookie/Authorization/<other>/None] and token_type=[preaccess/verification/grant/access].

 	Lambda functions:
 	 Step 1:
	 	locate:
	 		Goal find a token raw data based on the location, using the lambda search function, then having found the raw data - create an instance of a Token, based on that raw data.
	 	 	Arguments: l - location ; h - headers.
	 	 	First step - get <l> in the <h> : if there is one proceed to the next step, otherwise return {location:None,raw:None}
	 	 	Second step - initialize an instance of Token Class, by passing the raw_data, which is the result of the token_raw_data lambda function -> which based on the location , calls the search function with appropriate arguments, which are also based on the
	 	 	intially passed location. Thus returning a first matching 
	 	 	Return {'location':<l>,object:<Token>}

	 	search:
	 	 	Goal - using the regex search function , look for the <first matching case> , based on the <head>
	 	 	Arguments: head - field heading : ie "Bearer "/"grant_token=" , raw - raw data.
			Return <first matching case>:str or None

		 token_raw_data:
		 	Goal - select proper payload for the search function , based on the location.
		 	Arguments l - location , d - data
		 	Return ('Bearer '/'<token_type>=',d) / d
	 
	 Step 3.2:
	 	[Note flow works from buttom up!]

	 	find_case:
	 		Goal:find the very first case , when a pair of provided credentials, actually stored a UserService in a map object and not a None.
	 		Thus find the very first case of valid identification data -> respected UserService.
	 		Arguments: cases:map object.
		 		[Note] In order to prevent any errors, also expect a case when the user could have terminated the account , when the token was still valid.
		 		Thus after filtering the map object for any non None items, store the result in a tuple and:
		 		If the tuple is empty - return None
		 		Otherwise return the next item from the tupled value, converting it into an iterable. 
		 	Returns: UserService|None.

	 	map_cases:
	 		Goal: map 2 cases based on the provided credentials - a User Service for a username and an email.
	 		Arguments:credentials:key-word-argument , shall consist of keys: username and email.
	 		While iterating, store the UserService instance with a respected credential payload , if the UserService's inner instance - exists - thus the user exists, otherwise store None.
	 		Returns: map object, which consists UserService instances | None.
		
	 	resolve_user:
	 		Goal: find a legal/already singed up UserService of a user.
	 		Arguments: identification:kwargs - a dictionary of some unique data , could be a username or an email.
	 		With the help of map_cases - map each possible case for the UserService , then find the very first case, which matches the identification , with the find_case.
	 		Returns: UserService|None

		valid_verification:
			Goal: verify the current_token_version in the provided verification token, based on the verification data. In other words : the current_token_version must be equal to the last assigned one - the one in the database(login) | 0 (signup).
			[At this point the signature is valid - the validation in this instance, solves the problem of reusing the verification tokens, by denying the already used ones - using the current_token_version and provided identification_data]
			Agruments:t:dict(location:<location field:str|None>,object:<object instance:Token|None>)
			Actions:
				1.Extract the preaccess token from the provided verification token -> getting the initial route.
				2.Figure out the route and resolve the user based on the submited identification data and the initial route itself, with the help of resolve_user.
				3.Having established the resolved_user:
					If the route was signup:
						If resolved_user was found - then set the <condition> to fail ~> (None != current_token_version == None) => False.
						Otherwise set the <condition> to verify: (None != current_token_version == 0) => True|False
					Otherwise the route was login:
						If resolved_user wasn't found - then set the <condition> to fail ~> (None != current_token_version == None) => False.
						Otherwise set the <condition> to verify: (None != current_token_version == resolved_user's token_version) => True|False
				4. Having set up the condition:
					If the condition is valid:
						Return {'valid':True,'status_code':200}
					Otherwise return {'valid':False,'status_code':401} - impyling that the token was invalid/used - and from this point the token could be used for the requests.
			Returns: dictionary(valid:bool,status_code:int)

		valid_ownership:
			Goal: verify whether the ownership of the token (acesss|grant) is up to the current token version.
			[This solves the problem of reusing the acesss|grant tokens, by denying the already used ones]
			Agruments:t:dict(location:<location field:str|None>,object:<object instance:Token|None>)
			Actions:
				1.The access|grant token shall contain the user_id -> which is used to establish a UserService instance of the user.
				2.Having done that, verify the accord between the provided token_version and the one that UserService possess.
				If the versions are equal:
					Return a dictionary with plugged in revealed owner - {'valid':True,'status_code':200, 'owner':owner}
				Otherwise the token has been already used, return a dictionary with the owner as None - {'valid':False,'status_code':401, 'owner':owner}
			Returns: dictionary(valid:bool,status_code:int,owner:UserService|None)



	Validation:
 		1.Look for a token in a location. If location is set - direct the search at the <location>, otherwise search in Authorization/Cookie. If the token is present and valid , set authorization={token:<token>} proceed to the next step.
 		[-]If token object is invalid or doesn't correspond to the passed token_type - set authorization={'valid':False,status_code:401,'token':<token>} - resume to the Return Phase.
 		2.If the token_type is in ('access','grant') -> proceed to step 3.1
 		[-]Otherwise  if the token_type is the 'verification' one -> proceed to step 3.2
 		[-]Otherwise set authorization={'valid':True,status_code:200,'token':<token>} and proceed to the Return Phase.

 		3.1.Validate the existance of the "user_id" (owner), "token_version" (last granted version) keys in the token's dictionary, according to the user_id, find the assumed owner ~> using UserService instance , where (id=token[user_id])
 		Then if the owner exists , check the accord of the token_version in the token with the one in the Data Base. if the ownership matches insert another key 'owner' and assign a UserService instance 
 		[-]Otherwise set authorization={'valid':False,status_code:401}

 		3.2.Extract the preaccess_token, and establish the initial_route = "signup/login":
 			If the initial_route is "signup" -> verify that there is no existing user with such identification data, if there is, set condition for a failure, otherwise set condition to verify with a 0.
 			Otherwise the initial_route must be 'login' -> then there must be a legal user , perform a search for them. Then if the user exists , verify that current_token_version from the verification_token is equal to the one that legal user posesses.
 		[-]If any conditions turns out to be false - set authorization={'valid':False,status_code:401}


 	 Exceptions:
 	 	If the <token_type> is not a string , raise TypeError
 	 	If the <location> is not None or not a string, raise TypeError

 	 	If the len(args)<=1 - thus there in no headers, raise Exception
 	 	If the headers is not a dictionary , raise TypeError
 	 	IF the authorization chain is not empty and it already contains the <token_type>, raise appropriate Exception

 	Return: route(*args,*kwargs), where kwargs shall be updated with authorization[<token_type>]={valid:<True/False>,status_code:<200/401>,token:<{location:<location/None>,object:<Token/None>}>, if the token is a grant/access + owner:<UserService/None>}
	'''
#Code:
	#Exceptions
	assert isinstance(token_type,str), TypeError('"token_type" must be a string.')
	assert isinstance('' if location is None else location,str), TypeError('"location" must be a string or None.')

	def decorator(route):
		@wraps(route)
		def validate(*args,**kwargs):

			#Exceptions
			assert len(args)>1, Exception('No headers has been found.')
			assert isinstance((headers:=args[1]),dict), TypeError('Headers must be a dictionary.')
			assert (True if (authorization:=kwargs.pop('authorization',{token_type:{}}))=={token_type:{}} else (True if authorization.get(token_type,None) is None else False)), Exception(f'"{token_type}" is already in the authorization chain.')
			
			#Validation

			#Initialize lambda functions for the 1.:
			search = lambda head,raw: match.group() if (match:=re.search(f'(?<={head})([^\s]+)',raw)) else None
			token_raw_data = lambda l,d: search('Bearer ',d) if l=='Authorization' else (search(f'{token_type}_token=',d) if l=='Cookie' else d)
			locate = lambda l,h: {'location':l, 'object':Token(raw_data=token_raw_data(l,raw) ) } if (raw:=h.get(l)) else {'location':l,'object':None}
			
			#Initialize lambda functions for the 3.2:
			find_case = lambda cases: next(iter(tupled)) if (tupled:=tuple(filter(lambda case: case is not None,cases))) else None
			map_cases = lambda **credentials: map(lambda identification: case if (case:=UserService(**{identification:credentials[identification]})).id else None,credentials)
			resolve_user = lambda **identification: find_case(map_cases(**identification))
			
			either = auth_field_case if (auth_field_case:=locate('Authorization',headers)).get('object') else (cookie_field_case if (cookie_field_case:=locate('Cookie',headers)).get('object') else {'location':None,'object':None})
			#Validation:1.
			if (token:=locate(location,headers) if location else either)['object'] and token['object'].is_valid and token['object']['token_type']==token_type:
				#Validation:2.
				#Validation:3 ~> valid_ownership|valid_verification.

				valid_verification = lambda t : {'valid':True,'status_code':200} if \
				( None!=t['object']['current_token_version'] ==\
					( (None if (resolve_user(username=(identification:=t['object']['identification_data'])['username'],email=identification['email'])) else 0 )\
					if (preaccess:=Token(raw_data=t['object']['preaccess']))['route']=='signup' else\
					(resolved_user.token_version if (resolved_user:=resolve_user(username=(identification:=t['object']['identification_data']['identification']),email=identification)) else None) ) \
				)\
				else {'valid':False,'status_code':401}

				
				valid_ownership = lambda t: {'valid':True,'status_code':200, 'owner':owner} if (owner:=UserService(id=t['object']['user_id'])).token_version==t['object']['token_version'] is not None else {'valid':False,'status_code':401, 'owner':None}
				
				authorization[token_type] = {'token':token, **(valid_ownership(token) if token_type in ('grant','access') else (valid_verification(token) if token_type=='verification' else {'valid':True,'status_code':200} ) )}

			else:
				authorization[token_type] = {'valid':False,'status_code':401,'token':token}

			return route(*args,**{**kwargs,'authorization':authorization})

		return validate

	return decorator
