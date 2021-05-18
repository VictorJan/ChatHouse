from chathouse.models import db,Keyring
from copy import deepcopy

class KeyringService:
	def __init__(self,**identification):
		'''
		Parameters: identification is a key word argument, that shall only include proper unique keys.
		'''
		self.__instance=self.__identify(**identification)


	def create(self,**payload):
		'''
		Goal: create a keybundle of a certain user defined by their owner_id.
		Parameters: payload - a key word argument, that shall only contain data appropriate for the Keyring table constraints.
		Return : True/False:bool - which indicates the result of the creation.
		Exceptions: 
			ValueError is raised , if:
				- the payload doesn't contain the fixed amount of keys | the keys don't correspond to the neccessary ones | the data types of the values , of the mentioned keys are invalid.
			perform a rollback of the session and return False, if the payload wasn't appropriate.
		'''
		resolve_data_type=lambda key: int if key in ('owner_id','public_key') else dict
		
		assert len(payload)==3 and all(map(lambda key: key in payload and isinstance(payload[key],resolve_data_type(key)), ('owner_id','public_key','private_key'))),ValueError('The payload must contain keys for "owner_id","public_key","private_key".')
		
		if self.__instance is None and all(map(lambda key: key in payload['private_key'] and isinstance(payload['private_key'][key],str) ,('iv','data'))):
			#try:
				self.__instance=Keyring(**payload)
				db.session.add(self.__instance)
				db.session.commit()
				db.session.refresh(self.__instance)
				return True
			#except:
				self.__instance=None
				db.session.rollback()
				return False
		return False


	def __getattr__(self,attr):
		return ( deepcopy(value) if (value:=self.__instance.__dict__.get(attr,None)) is not None else value ) if self.__instance else None

	def remove(self):
		if self.__instance:
			try:
				db.session.delete(self.__instance)
				db.session.commit()
				return True
			except:
				db.session.rollback()
				return False
		return False

	@staticmethod
	def __identify(**payload):
		'''
		Parameters: payload is a key word argument, that's used to filter the Keyring table.
		Exceptions:
			SyntaxError - raised when the payload doesn't contain only one identification key.
			KeyError - raised when the identification key is not appropriate according to the Table constaints
		'''
		assert len(payload)==1, SyntaxError('The initialization of the instance may accept only 1 identification at a time.')
		assert any(map( lambda key: key in payload, ('id','owner_id','public_key'))) , KeyError('The identification payload doesn\'t correspond to any of the unique keys.')

		return Keyring.query.filter_by(**payload).first()


		