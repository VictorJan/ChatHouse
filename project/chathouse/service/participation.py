from chathouse.models import db,Participation
import chathouse.service as service
from copy import deepcopy

class ParticipationService:
	'''
	The  PaticipationService defines required methods and properties, necessary to perform any CRUD and other actions related to the Participation instances.

	Methods:
		create(self,**payload) - estalishes/create an inner participation instance , based on the provided payload.
		remove(self) - remove the inner instance.
		refresh(self) - refreshes the inner state of the instance.
	Dunder methods:
		init(self,**identification) - initializes the current user service instance, based on the provided identificaiton payload.
		getattr(self,attr) - searches the inner instance attribute for the provided attr argument.
	Properties:
		participant - returns a user service object of a related user-participant.
	Static methods:
		__identify(**identification) - identifies a current participant instance based on the provided unique identification payload.
		
	'''
	def __init__(self,**identification):
		'''
		Arguments: identification is a key word argument, that shall only include proper unique keys. 
		'''
		self.__instance=self.__identify(**identification) if identification else None


	def create(self,**payload):
		'''
		Goal: create an instance of the Participation based on the identifications of a participant and a chat.
		Arguments: payload - a key word argument, that shall only contain data appropriate for the Keyring table constraints.
		Returns : True/False:bool - which indicates the result of the creation.
		Exceptions: perform a rollback of the session and return False, if the payload wasn't appropriate.
		'''
		assert len(payload)==2, Exception('The signup requires the payload to consist of two keys.')
		assert all(map( lambda key: key in payload and isinstance(payload[key],int), ('chat_id','participant_id'))) , ValueError('The payload must contain a chat_id:<int> and a participant_id:<int>.')

		if self.__instance is None and service.UserService(id=payload['participant_id']).get_a_chat(payload['chat_id']) is None:
			try:
				self.__instance=Participation(**payload)
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
		return False

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


	def __getattr__(self,attr):
		'''
		Goal: get the attribute from the inner instance.
		Arguments: attr:str
		Actions:
			Based on the provided attr value - search the inner instance dictionary for such attribute.
			If the value coulnd't have been found - refresh the inner instance and perform the search again, then return the value in either way.
			Otherwise return the value
		Returns: value(based on the attr from the inner instance) | None
		'''
		get = lambda attribute: deepcopy(value) if (value:=self.__instance.__dict__.get(attribute,None)) else None
		return ( get(attr) if (value:=get(attr)) is None and self.refresh() else value ) if self.__instance else None

	@property
	def participant(self):
		return service.UserService(id=self.__participant.id) if self.__instance else None
	

	@staticmethod
	def __identify(**payload):
		'''
		Arguments: payload is a key word argument, that's used to filter the Keyring table.
		Returns: Instance of the Partication class / None.
		Exceptions:
			SyntaxError - raised when the payload doesn't contain only one identification key.
			KeyError - raised when the identification key is not appropriate according to the Table constaints
		'''
		assert len(payload)==1, Exception('The initialization of the instance may accept only 1 identification at a time.')
		assert any(map( lambda key: key in payload and isinstance(payload[key],int), ('id',))) , Exception('The identification payload doesn\'t correspond to any of the unique keys.')

		return Participation.query.filter_by(**payload).first()


		