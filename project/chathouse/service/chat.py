from chathouse.models import db,Chat,Message,Participation
import chathouse.service as service

from copy import deepcopy
import time,datetime

class ChatService:
	def __init__(self,**identification):
		'''
		Parameters: identification is a key word argument, that shall only include proper unique keys.
		'''
		self.__instance=self.__identify(**identification) if identification else None


	def create(self,**payload):
		'''
		Arguments: payload - a key word argument, that shall only contain data appropriate for the Chat table constraints.
		Return : True/False:bool - which indicates the result of the creation.
		Exceptions: perform a rollback of the session and return False, if the payload wasn't appropriate.
		'''
		resolve_data_type=lambda key: int if key=='creator_id' else str
		
		assert len(payload)==2 and all(map(lambda key: key in payload and isinstance(payload[key],resolve_data_type(key)), ('creator_id','name'))),ValueError('The payload must contain keys for "creator_id", "name".')
	
		if self.__instance is None:
			try:
				self.__instance=Chat(**payload)
				db.session.add(self.__instance)
				db.session.commit()
				db.session.refresh(self.__instance)
				return True
			except:
				self.__instance=None
				db.session.rollback()
				return False
		return False

	def delete(self,**payload):
		pass

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

	def get_message(self,**query):
		'''
		Goal: Query the Chat table to find a user/users , using the like statement.
		Arguments: query - a key word argument, expecting keys: "dnt","amount".
		'''

		assert (dnt:=query.get('dnt',int(time.time()))) is not None and (amount:=query.get('amount',15)) is not None and all(map(lambda q: isinstance(query[q],int) and q>0),query), SyntaxError('Invalid query parameters.')
		
		return [service.MessageService(id=message.id) for message in self.__instance.messages.filter(Message.dnt>datetime.datetime.fromtimestamp(dnt)).order_by(Message.dnt).limit(amount)] if self.__instance else None


	def __getattr__(self,attr):
		return ( deepcopy(value) if (value:=self.__instance.__dict__.get(attr,None)) is not None else value ) if self.__instance else None

	@property
	def participants(self):
		return [service.UserService(id=participant.id) for participant in self.__instance.participants ] if self.__instance else None
	


	@staticmethod
	def __identify(**payload):
		'''
		Parameters: payload is a key word argument, that's used to filter the Chat table.
		Exceptions:
			SyntaxError - raised when the payload doesn't contain only one identification key.
			KeyError - raised when the identification key is not appropriate according to the Table constaints
		'''
		assert len(payload)==1, SyntaxError('The initialization of the instance may accept only 1 identification at a time.')
		assert any(map( lambda key: key in payload, ('id','name'))) , KeyError('The identification payload doesn\'t correspond to any of the unique keys.')

		return Chat.query.filter_by(**payload).first()