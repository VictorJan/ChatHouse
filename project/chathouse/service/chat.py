from chathouse.models import db,Chat,Message
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

	def remove(self):
		'''
		Goal: removes the inner instance from the database.
		Returns:True if the inner instance exists and there hasn't been any session execution exception Otherwise False. 
		'''
		if self.__instance:
			try:
				db.session.delete(self.__instance)
				db.session.commit()
				return True
			except:
				db.session.rollback()
		return False

	def get_message(self,**query):
		'''
		Goal: Query the Chat table to find a user/users , using the like statement.
		Arguments: query - a key word argument, expecting keys: "dnt","amount".
		Actions:
			If dnt or amount is not submited - respectfuly set the values as current time and 15.
			Filter messages of the inner instance : where the date n time of the message is lesser than the submited dnt, converted into datetime instance - thus getting the older messages since the provided dnt.
			The values are odered by the descending inner dnt values.Furthermore - the amount of the values is limited by the provided amount. 
			Having done the retrieval, iterate through each of the messages and store the MessageService of each message.
		Returns: tuple(MessageService instance of filtered inner messages) if the inner instance exists , otherwise None
		Exceptions:
			Raises:
				SyntaxError - if the submited query parameters : dnt,amount - are not integers or lesser than|equal zero.
			Return None:
				In case of OverflowError - occuring during the dnt conversion into datetime instance.
				In any other arising expection ,occuring during the dnt conversion.
		'''
		assert (dnt:=query.get('dnt',int(time.time()))) is not None and (amount:=query.get('amount',15)) is not None and all(map(lambda q: isinstance(q,int) and q>0,(dnt,amount))), SyntaxError('Invalid query parameters.')
		
		try:
			dnt=datetime.datetime.fromtimestamp(dnt)
		except OverflowError:
			return None
		except:
			return None
		
		return tuple(service.MessageService(id=message.id) for message in self.__instance.messages.filter(Message.dnt<dnt).order_by(Message.dnt.desc()).limit(amount)) if self.__instance else None

	def refresh(self):
		'''
		Goal: refreshes state of the inner instance.
		Returns:True if the inner instance exists and there hasn't been any exceptions Otherwise False. 
		'''
		if self.__instance:
			try:
				db.session.refresh(self.__instance)
				return True
			except:
				pass
		return False

	@property
	def participations(self):
		'''
		Goal:return a tuple of the participations.
		Returns:tuple(of ParticipantServices for each participation of the chat) If the inner instance exists else None
		'''
		return tuple(service.ParticipationService(id=participation.id) for participation in self.__instance.participations.all()) if self.__instance else None
	
	@property
	def participants(self):
		'''
		Goal:return a tuple of the participants.
		Returns:tuple(of UserServices for each participant of the chat) If the inner instance exists else None
		'''
		return tuple(service.UserService(id=participation.participant_id) for participation in self.__instance.participations.all()) if self.__instance else None
	

	@property
	def creator(self):
		'''
		Goal:return a creator of the chat.
		Returns:UserService of the creator If the inner instance exists else None
		'''
		return service.UserService(id=self.__instance.creator.id) if self.__instance else None
	

	def __getattr__(self,attr):
		return ( deepcopy(value) if (value:=self.__instance.__dict__.get(attr,None)) is not None else value ) if self.__instance else None


	@staticmethod
	def __identify(**payload):
		'''
		Parameters: payload is a key word argument, that's used to filter the Chat table.
		Exceptions:
			SyntaxError - raised when the payload doesn't contain only one identification key.
			KeyError - raised when the identification key is not appropriate according to the Table constaints
		'''
		assert len(payload)==1, SyntaxError('The initialization of the instance may accept only 1 identification at a time.')
		assert any(map( lambda key: key in payload and isinstance(payload[key],int), ('id',))) , KeyError('The identification payload doesn\'t correspond to any of the unique keys.')
		return Chat.query.filter_by(**payload).first()
