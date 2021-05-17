from chathouse.utilities.security.token import Token
from chathouse.service import UserService,ChatService
from functools import wraps
import re

def authorized(token_type,location=None):
	'''
	Validate authorization, relying on the JWT tokens, that could be passed to <location>=[Cookie/Authorization/<other>/None] and <token_type>=[preaccess/verification/grant/access].
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

	Validation:
 		1.Look for a token in a location. If location is set - direct the search at the <location>, otherwise search in Authorization/Cookie. If the token is present and valid , set authorization={token:<token>} proceed to the next step.
 		[-]If token object is invalid or doesn't correspond to the passed token_type - set authorization={'valid':False,status_code:401,'token':<token>} - resume to the Return Phase.
 		2.If the token_type is in ('access_token','grant_token') -> proceed to step 3.
 		[-]Otherwise set authorization={'valid':True,status_code:200,'token':<token>} and proceed to the Return Phase.
 		3.Validate the existance of the "user_id" (owner), "token_version" (last granted version) keys in the token's dictionary, according to the user_id, find the assumed owner ~> using UserService instance , where (id=token[user_id])
 		Then if the owner exists , check the accord of the token_version in the token with the one in the Data Base. if the ownership matches insert another key 'owner' and assign a 
 		[-]Otherwise set authorization={'valid':False,status_code:401}


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

			#Initialize lambda functions
			search = lambda head,raw: match.group() if (match:=re.search(f'(?<={head})([^\s]+)',raw)) else None
			locate = lambda l,h: {'location':l, 'object':Token(raw_data=token_raw_data(l,raw) ) } if (raw:=h.get(l)) else {'location':l,'object':None}
			token_raw_data= lambda l,d: search('Bearer ',d) if l=='Authorization' else (search(f'{token_type}_token=',d) if l=='Cookie' else d)
			
			either = auth_field_case if (auth_field_case:=locate('Authorization',headers)).get('object') else (cookie_field_case if (cookie_field_case:=locate('Cookie',headers)).get('object') else {'location':None,'object':None})
			#Validation:1.
			if (token:=locate(location,headers) if location else either)['object'] and token['object'].is_valid and token['object']['token_type']==token_type:
				#Validation:2.
				#Validation:3 ~> valid_ownership.
				#valid_ownership is valid if User with id of token['object']['user_id'] exists , and the token_version is equal to the one in the token
				valid_ownership = lambda t: {'valid':True,'status_code':200, 'owner':owner} if (owner:=UserService(id=t['object'].user_id)).token_version==t['object']['token_version'] is not None else {'valid':False,'status_code':401, 'owner':None}
				authorization[token_type] = {'token':token, **(valid_ownership(token) if token_type in ('grant_token','access_token') else {'valid':True,'status_code':200} )}
			else:
				authorization[token_type] = {'valid':False,'status_code':401,'token':token}

			return route(*args,**{**kwargs,'authorization':authorization})

		return validate

	return decorator
