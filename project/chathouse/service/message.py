from chathouse.models import db,Message
import chathouse.service as service
from copy import deepcopy

class MessageService:
	def __init__(self,**identification):
		'''
		Arguments: identification is a key word argument, that shall only include proper unique keys. 
		'''
		self.__instance=self.__identify(**identification) if identification else None


	def create(self,**payload):
		'''
		Goal: create a Message instance , depending on the provided payload.
		Arguments: payload - a key word argument, that shall only contain data appropriate for the Message table constraints.
		Expecting: chat_id:<int>,sender_id:<int>,content:{iv:<str>,data:<str>}
		Actions: Verify : the absence of the current message instance, make sure that the provided sender is a participant of the provided chat, using the identifications. Also make sure that the content consists of the necessary keys for the decryption.
		Then proceed to create a Message instance, updating the date n time activity value of the related chat.
		Returns : True/False:bool - which indicates the result of the creation.
		Exceptions:
			Raises:
				ValueError is raised, if:
					- the payload doesn't contain the fixed amount of keys | the keys don't correspond to the necessary ones | the data types of the values , of the mentioned keys are invalid.
			Perform a rollback of the session and return False, if the payload wasn't appropriate.
		'''

		resolve_data_type=lambda key: int if key in ('chat_id','sender_id') else dict
		
		assert len(payload)==3 and all(map(lambda key: key in payload and isinstance(payload[key],resolve_data_type(key)), ('chat_id','sender_id','content'))),ValueError('The payload must contain keys for "chat_id":<int> , "sender_id":<id> and "content":<dict>.')
		
		if self.__instance is None and service.UserService(id=payload['sender_id']).get_a_chat(payload['chat_id']) and all(map(lambda key: key in payload['content'] and isinstance(payload['content'][key],str) ,('iv','data'))):
			try:
				self.__instance=Message(**payload)
				db.session.add(self.__instance)
				
				db.session.flush()
				self.__instance.chat.activity_dnt=self.__instance.dnt
				
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
		Actions: Verify : the existance of the current message instance, then proceed to delete the inner instance, updating the date n time activity value of the related chat.
		Returns:True if the inner instance exists and there hasn't been any session execution exception Otherwise False. 
		'''
		if self.__instance:
			try:
				
				self.__instance.chat.activity_dnt=self.__instance.dnt

				db.session.delete(self.__instance)

				db.session.commit()
				return True
			except:
				db.session.rollback()
				return False
		return False

	def __getattr__(self,attr):
		return ( deepcopy(value) if (value:=self.__instance.__dict__.get(attr,None)) is not None else value ) if self.__instance else None

	@property
	def chat(self):
		'''
		Goal:return the chat which contains current message.
		Returns:ChatService of the chat If the inner instance of the message exists else None
		'''
		return service.ChatService(id=self.__instance.chat_id) if self.__instance else None

	@property
	def sender(self):
		'''
		Goal:return the sender of the current message.
		Returns:UserService of the user If the inner instance of the message exists else None
		'''
		return service.UserService(id=self.__instance.sender_id) if self.__instance else None
	

	@staticmethod
	def __identify(**payload):
		'''
		Arguments: payload is a key word argument, that's used to filter the Message table.
		Returns: Instance of the Message class / None.
		Exceptions:
			SyntaxError - raised when the payload doesn't contain only one identification key.
			KeyError - raised when the identification key is not appropriate according to the Table constaints
		'''
		assert len(payload)==1, Exception('The initialization of the instance may accept only 1 identification at a time.')
		assert any(map( lambda key: key in payload and isinstance(payload[key],int), ('id',))) , Exception('The identification payload doesn\'t correspond to any of the unique keys.')

		return Message.query.filter_by(**payload).first()



		