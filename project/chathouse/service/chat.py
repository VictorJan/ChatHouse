from chathouse.models import db,Chat,Message
import chathouse.service as service
from copy import deepcopy
import time,datetime

class ChatService:
	'''
	The ChatService defines required methods and properties, necessary to perform any CRUD and other actions related to the Chat instances.

	Methods:
		create(self,**payload) - estalishes/create an inner chat instance , based on the provided payload.
		remove(self) - remove the inner instance.
		refresh(self) - refreshes the inner state of the instance.
		get_message(self,**query) - gets any messages that fit the provided query, which involves searching for message based on the date n time - retrieving a provided amount, provided in the query.
	Dunder methods:
		init(self,**identification) - initializes the current chat service instance, based on the provided identificaiton payload.
		getattr(self,attr) - searches the inner instance attribute for the provided attr argument.
		contains(self,other) - verifies if the a user|message is related to the current chat. 
	Properties:
		creator - returns a user service object of a chat creator.
		participations - returns a tuple of participation services, related to the current chat.
		participants - returns a tuple of user services - of users related to a the chat, via a participation links.
		messages - returns a tuple of message services - of messages , that are contained in the chat.
	Static methods:
		__identify(**identification) - identifies a current chat instance based on the provided unique identification payload.
		
	'''
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

	def __contains__(self,other):
		'''
		Goal: verify if the other instance is contained in the Chat.
		Argumets: other:MessageService|UserService
		Actions:
			If there is an inner instance:
				Execute the resolve function -> which initiates the flow and returns the proper boolean.
			Otherwise return False.
		Variablies:
			implemented:tuple( of tuples that contain : [integrated XService],[searching scope],[identification key])
			[X] = User|Message
		
		Lambda functions:
			[Note flow works from buttom up!]

			filter_payload:
				Goal: construct a dictionary payload, based on the provided key,data values.
				Argumets: key:str, data:int - expected data types.
				Returns: dictionary:(of a provided key/value pair) if the arguments follow the guidelines for the data types , othewise an empty dictionary.

			proper_service_filter:
				Goal: resolve a proper [X]Service instance, from the implemented ones and perform the according filter.
				Arguments: instance:MessageService|UserService
				Actions:
					[At this point the provided "other" argument exists in the implementations - thus the following iteration will not return an Exception]
					Iterate through the implementation tuple - finding the very first service that matches the instance value.
					Having found that x_service -> perform a filter query , based on the [searching scope], providing the payload from the filter_payload , passing in the [identification key] and the id of the "other" argument.
				Returns: filter query instance.

			query:
				Goal: having established a filter instance according to the provided, implemented "other" instance, return the very first instance from the metioned filter query.
				Arguments: instance:XService
				Actions:
					Perform a call to the proper_service_filter which shall return properly established filter query, then return the first found instance.
				Returns: [X] model instance | None.

			resolve:
				Goal: resolve the request : "is the [instance] exists in the current chat".
				Arguments: instance:XService
				Actions:
					With the help of query function, which get's the first model instance from the filter query (if there is any), return the boolean decision.
				Returns: True if the query has returned an [X] model instance, otherwise False.

		Returns:bool - implying the existance of the [other] in a chat
		'''
		if self.__instance:

			implemented = (\
				(service.UserService,self.__instance.participations,'participant_id'),\
				(service.MessageService,self.__instance.messages,'id')\
				)

			assert any(map(lambda allowed: isinstance(other,allowed[0]) and other.id is not None ,implemented)) , NotImplementedError('The instance of the "other" argument shall only be either UserService or MessageService with existing inner instances.')

		
			filter_payload = lambda key,data: {key:data} if isinstance(key,str) and isinstance(data,int) else {}

			proper_service_filter = lambda instance: (x_service:=next(filter(lambda case:isinstance(instance,case[0]) ,implemented)))[1].filter_by(**filter_payload(x_service[2],instance.id))

			query = lambda instance: proper_service_filter(instance).first()
			
			resolve = lambda instance: True if query(instance) else False
			
			return resolve(other)

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
	def messages(self):
		return tuple(service.MessageService(id=message.id) for messages in self.__instance.messages.all()) if self.__instance else None
	

	@property
	def creator(self):
		'''
		Goal:return a creator of the chat.
		Returns:UserService of the creator If the inner instance exists else None
		'''
		return service.UserService(id=self.__instance.creator.id) if self.__instance else None


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
