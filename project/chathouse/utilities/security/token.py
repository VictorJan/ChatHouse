from flask import current_app
from hashlib import sha256
from base64 import urlsafe_b64decode
import jwt,json,datetime

class Token:
	'''
	Token - a class that could persist tokens, by generating or importing them. Also is abile to verify the token using the is_valid property.
	Apart from that is able to retrieve data from the payload, without performing the verification/validation.
 	
	Methods:
		__generate - generates the
	'''
	def __init__(self,**incoming_data):
		'''
		Goal: initialize a token instance based on the incoming data.
		Arguments:incoming_data:key-word-argument:dict.
		Actions:
			Token shall be initialized in two ways:
			- providing raw data , thus requiring a raw_data key , of value:str|None.
			- providing payload data, requiring a payload_data key /w value:dict, which would initiate a generation & signing of a token.
			[Note raw_data - could happen to contain a None - in such instances , value is assigned as None also.]
		Returns: None.
		Exceptions:
			Raises:
				ValueError - in case if the incoming_data payload couldn't be resolved to initialize a Token - the key-word-argument didn't follow the guidelines raw_data:str|None or payload_data:dict.
				Exception - if the configuration of the app doesn't contain a STATIC_KEY.

		'''
		guidelines = ( ('raw_data',(str,type(None))), ('payload_data',dict) )

		assert (key:=current_app.config.get('STATIC_KEY',None)) is not None, Exception('The configuration must contain a STATIC_KEY.')

		assert len(incoming_data)==1 and any( (resolved:={case[0]:value}) for case in guidelines if (value:=incoming_data.get(case[0],False)) is not False and  isinstance(value,case[1]) ),\
		ValueError('Invalid incoming_data key-word-argument. The key-word-argument shall contain one key at a time and such key must follow the guidelines: raw_data:str|None , payload_data:dict.')

		self.__static_key = key
		
		self.__value = raw if (raw:=resolved.get('raw_data',False)) is not False else self.__generate(**resolved['payload_data'])

	def __generate(self,**payload):
		'''
		Goal: encode and sign a token, which shall contain provided payload.
		Arguments:payload - key-word-argument.
		Actions:
			1.Get the current utc time, which then shall be converted to a float timestamp - the dnt of Token request/appeal.
			[Note: an integral part of signing a Token]
			2.If the payload contains an 'exp' key - set up the expiration as current dnt time + requested expiration amount.
			[Note: the value for the provided expiration has to be a dictionary of {minutes/hours/seconds:[value]} - that shall be valid for the datetime.timedelta(**exp)]
			Otherwise, set expiration to current time + 5 minutes.
			3.Then proceed to derive a unique symmetric key (based on the timestamp of the current date and time - the dnt value) to sign the payload, usign the HS256 algorithm.
		Returns: a signed JWT token:str.
		Exceptions:
			Raises:
				ValueError - in case the provided expiration value is invalid.
		'''
		
		try:
			payload['exp']=(dnt:=datetime.datetime.utcnow())+datetime.timedelta(**(payload.get('exp',{'minutes':5})))
		except Exception as exception:
			raise ValueError(f'The expiration value shall follow the timedelta guidelines. Precise/Exact reason - {exception}')

		payload['dnt']=datetime.datetime.timestamp(dnt)
		
		return jwt.encode(payload,self.__derive_a_key(payload['dnt']),algorithm='HS256')

	def __derive_a_key(self,dnt):
		'''
		Goal: establish a unique/one-off key (based on the provided timestample of the Token request) , which is used to sign the Token.
		Arguments:dnt:float - timestamp value of the Token appeal.
		Actions:
			Combine the static_key and the provided dnt/timestamp value - using the combine function /w digesting the values.
		Return: the conjunction (of the static_key and the timestamp of the appeal)
		Lambda functions:
			digest:
				Goal:sha256 digest the provided argument
				Argument: x:str
				Returns hex digest of sha256 function:str.

			combine:
				Goal:perform the conjuntion of provided arguments:
				Arguments: x:str , y:str.
				Actions: digest( digest(x) & digest(y) ) - & performs for each pair of bits.
				Returns: hexdigested value:str
		'''
		digest=lambda x: sha256(str(x).encode()).hexdigest()
		combine=lambda x,y: digest(''.join(iter(map(lambda pair: chr(pair[0]&pair[1]),zip( bytearray.fromhex(digest(x)) ,bytearray.fromhex(digest(y)))))))
		return combine(dnt,self.__static_key)

	@property
	def is_valid(self):
		'''
		Goal: verifies the validity of the intiated Token value.
		Actions:
			1.Verifies existance of the value;
			2.Make sure of dnt value - appeal timestamp, presence.
			3.Tries to decode the token , using the derived symmetric key , based on the conjuction of (static and dnt values).
			If either of the conditions fail - set whole validation fails , thus returns a False
			Otherwise returns a True
		Returns: True|False:bool
		Exceptions:
			In case of arrising expection related to decoding the token - verifying the signature, returns False.
		'''
		try:
			return True if self.__value and self['dnt'] and jwt.decode(self.__value,key=self.__derive_a_key(self['dnt']),algorithms=['HS256']) else False
		except:
			return False
		

	def __getitem__(self,key):
		'''
		Goal:retreive requested key from the payload of a JWT token, without executing the signature verification.
		Actions:
			Doesn't require the use of the signature key -> no need to derive a key.
 			Tries to : decode the payload part of the JWT structure , using urlsafe base64 and appropriate padding, then convert the data to a dictionary , using json.loads().
 			After that, get a value from the dictionary using the attr as a key.
 		Returns: value according to the key in the payload of the JWT token, if exists and structure of the token is appropriate, otherwise None
		'''
		try:
			pad=lambda data:f'{data}{(4-(len(data)%4))*"="}'
			return json.loads(urlsafe_b64decode(pad(self.__value.split('.')[1]))).get(key,None)
		except:
			return None

	@property
	def value(self):
		'''
		Goal: retreive the raw value of the token.
		Returns: value attribute:str.
		'''
		return self.__value
