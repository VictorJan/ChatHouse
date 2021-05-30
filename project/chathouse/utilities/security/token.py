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
			- providing raw data , thus requiring a raw_data key , of value:str.
			- providing payload data, requiring a payload_data key /w value:dict, which would initiate a generation & signing of a token.
			[Note raw_data - could happen to contain a None - in such instances , value is assigned as None also]
		Returns: None.
		Exceptions:
			Raises:
				Exception - if the configuration of the app doesn't contain a STATIC_KEY.
		'''
		assert (key:=current_app.config.get('STATIC_KEY',None)) is not None, Exception('The configuration must contain a STATIC_KEY.')
		
		self.__static_key=key
		
		self.__value = raw if (raw:=incoming_data.get('raw_data',None)) is not None else (self.__generate(**payload) if (payload:=incoming_data.get('payload_data',None)) is not None and isinstance(payload,dict) else None )

	def __generate(self,**payload):
		'''
		Goal: encode and sign a token, which shall contain provided payload.
		Arguments:payload - key-word-argument.
		Actions:
			First get the current utc time, which is an integral part of signing a token - the dnt of Token request.
			Then If the payload contains an 'exp' key - set up the expiration as current time + requested expiration amount.
			[Note that the value for the provided expiration has to be a dictionary of {minutes/hours/seconds:[value]} - that shall be valid for the datetime.timedelta(**exp)]
			Otherwise, set expiration to current time + 5 minutes.
			Then proceed to derive a unique symmetric key (based on the timestamp of the current date and time - the dnt value) to sign the payload, usign the HS256 algorithm.
		Returns: a signed JWT token:str.
		Exceptions:
			Raises:
				ValueError - in case the provided expiration value is invalid.
		'''
		
		try:
			payload['exp']=(dnt:=datetime.datetime.utcnow())+datetime.timedelta(**(payload.get('exp',{'minutes':5})))
		except Exception as exception:
			raise ValueError(f'The expiration value shall follow the timedelta guidelines. Precise/Exact exception - {exception}')

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
				Returns hex digest of sha256 function.

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
 			After that get a value from the dictionary using the attr as a key.
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
