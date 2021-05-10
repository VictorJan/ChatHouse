from hashlib import sha256
from copy import deepcopy
from base64 import b64decode
import jwt,json,datetime,time
import os


class Token:

	assert (__static_key:=os.environ.get('STATIC_KEY',None)) is not None, Exception('There must be a STATIC_KEY.')

	def __init__(self,**incoming_data):
		self.__value = raw if (raw:=incoming_data.get('raw_data')) else (self.__generate(**payload) if (payload:=incoming_data.get('payload_data')) else None)

	def __generate(self,**payload):
		payload['exp']=(dnt:=datetime.datetime.utcnow())+datetime.timedelta(**(payload.get('exp',{'minutes':5})))
		payload['dnt']=datetime.datetime.timestamp(dnt)
		return jwt.encode(payload,self.__derive_a_key(payload['dnt']),algorithm='HS256')

	def __derive_a_key(self,dnt):
		digest=lambda x: sha256(str(x).encode()).hexdigest()
		combine=lambda x,y: digest(''.join(iter(map(lambda pair: chr(pair[0]&pair[1]),zip( bytearray.fromhex(digest(x)) ,bytearray.fromhex(digest(y)))))))
		return combine(dnt,self.__static_key)

	@property
	def is_valid(self):
		try:
			return True if self.__value and self['dnt'] and jwt.decode(self.__value,key=self.__derive_a_key(self['dnt']),algorithms=['HS256']) else False
		except:
			return False
		

	def __getitem__(self,key):
		try:
			pad=lambda data:f'{data}{(4-(len(data)%4))*"="}'
			return json.loads(b64decode(pad(self.__value.split('.')[1]))).get(key,None)
		except:
			return None

	@property
	def value(self):
		return self.__value
	