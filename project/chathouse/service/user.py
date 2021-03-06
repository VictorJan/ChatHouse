from chathouse.models import db,User,Keyring,Chat,Participation,Message
import chathouse.service as service
from copy import deepcopy
from datetime import datetime
from time import time

class UserService:
	'''
	The  UserService defines required methods and properties, necessary to perform the Authenticaion,CRUD and other actions.
	
	Methods:
		remove(self,password=None) - remove the inner instance, performing a password verification, if submited.
		refresh(self) - refreshes the inner state of the instance.
		signup(self,**payload) - serves as a registration/signup tool, based on the provided payload.
		login(self,**payload) - performs a user login steps, based on the provided payload.
		password_reset(self,**payload) - serves as a password reset tool, based on the respective payload.
		update_activity(self) - updates the inner "activity state" - of the user.
		establish_a_chat(self,name) - creates a chat with a provided name.
		join_a_chat(self,identification) - executes steps, required to join a chat, based on the provided identification.
		dischage_a_chat(self,identification) - executes actions related to removing a chat, in cases when the current user is a participant of such chat.
		establish_a_message(self,**payload) - performs creation of a message, based on the provided payload.
		discharge_a_message(self,**payload) - removes a message (based on the provided data), in cases when the message exists in a chat - where user is stated as a participant.
		get_a_chat(self,identification) - searches for a chat ,with a certain identification, to which user is related/connected as a participant.
		common_ground_with(self,**identification) - looks up for common chats between the current user, and a user identified based on the provided identification key-word-argument.
	Dunder methods:
		init(self,**identification) - initializes the current user service instance, based on the provided identificaiton payload.
		getattr(self,attr) - searches the inner instance attribute for the provided attr argument.
	Properties:
		activity_state - returns current "activity state".
		keyring - returns a keyring service object of a related keyring instance.
		chats - returns a tuple of chat service objects, which are connected to a user , via participations.
	Static methods:
		__identify(**identification) - identifies a current user instance based on the provided unique identification payload.
		get(**query) - searches for a user based on the requested query - which would involve finding a user based on their username/name.
	'''
	def __init__(self,**identification):
		'''
		Arguments: identification is a key word argument, that shall only include proper unique keys.
		'''
		self.__instance=self.__identify(**identification) if identification else None
		
	def remove(self,password=None):
		'''
		Goal: remove the current instance of the User class.
		Arguments:password:None|str.
		Actions:
			If the inner instance exists, and if the password has been provided -> verify the relation between the current and provided passwords. If equal proceed to delete the instance, thus removing each related instance.
			Otherwise if the password wasn't provided -> proceed to delete the instance in either way.
		Returns: True/False:bool.
		Exceptions:
			TyperError - if the password is provided and the data type of which is not a string.
			In case of an arising exception , related to delete method, perform the session rollback.
		'''
		assert isinstance(password,str) if password is not None else True, TypeError('If submited, data type of the password argument shall be a string.')
		
		if self.__instance and (self.__instance.password==password if password is not None else True):
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


	def signup(self,**payload):
		'''
		Goal: perform a signup process for a user , creating an according keyring, a "selfchat" with proper "selfparticipation".
		Chain calls to :  self.join 

		Arguments: payload - a dictionary key word argument , which shall consist of 2 dictionaries: user_data and a key_data.
		Excpecting: user_data:{
			"username":<str>,
			"email":<str>,
			"name":<str>,
			"about":<str>,
			"password":<str>
		}
		key_data:{
			"public_key":<int>
			"private_key":<dict>
		}
		
		Actions:
			Verify non existance of the instance in the database.
			Create an instance, using submited user_data in the payload.
			If managed to create instances for a keyring, a chat and a participation : return True
			Otherwise : rollback the session for the add(user) and remove all of the instances and return False

		Returns: True/False : bool.

		Exceptions:
			Exception - raised when the provided payload doesn't consist of two keys.
			TypeError - raised when the payload doesn't contain required keys or the values are not of dictionary type.
			In case of an arising exception , related to the incorrect payload used in the session oparation , perform the session rollback.
		'''
	
		assert len(payload)==2, Exception('The signup requires the payload to consist of two keys.')
		assert all(map( lambda key: key in payload and isinstance(payload[key],dict), ('user_data','key_data'))) , ValueError('The payload must contain keys for "user_data" and "key_data" , which have to be dictionaries.')
		if self.__instance is None:
			try:
				self.__instance=User(**payload['user_data'])
				db.session.add(self.__instance)
				db.session.flush()

				payload['key_data']['owner_id']=self.__instance.id

				if (keyring:=service.KeyringService(owner_id=payload['key_data']['owner_id'])).create(**payload['key_data']) and (chat:=self.establish_a_chat('Saved Messages')).id and self.join_a_chat(chat.id):
					db.session.commit()
					self.refresh()
					return True

				else:
					db.session.rollback()
					
					if keyring.id is not None:
						chat.remove()
					
					keyring.remove()

					self.__instance=None

			except:
				
				db.session.rollback()
				self.__instance=None

		return False

	def login(self,**payload):
		'''
		Goal: perform a login process for a user.

		Arguments: payload - a dictionary key word argument , which shall consist of next 
		Excpecting: {
			password:<str> (already hashed)
		}
		
		Actions:
			Verify existance of the instance in the database.
			Check if the provided password matches the one in the database, an upgrade of the activity state has been successful : return True.
			Otherwise : return False

		Returns: True/False : bool.

		Exceptions:
			ValueError - raised when the provided payload doesn't consist of one necessary key.
			TypeError - raised when the payload doesn't contain required keys or the values are not of dictionary type.
			In case of an arising exception , related to the incorrect payload , perform the session rollback.
		'''

		assert len(payload)==1 and payload.get('password'), ValueError('The login requires the payload to consist of only one key - "password".')
		assert isinstance(payload.get('password',None),str) , TyperError('The payload must contain a password key, the value of which must be a string.')

		return True if self.__instance is not None and self.__instance.password==payload['password'] and self.update_activity() else False

	def reset_password(self,**payload):
		'''
		Goal: perform a password reset, based on the provided payload.

		Arguments: password - a dictionary key word argument , which shall consist of next 
		Excpecting: {
			password:{
				current:str (already hashed),
				new:str (already hashed)
			},
			private_key:{iv:str,data:str}
		}
		
		Actions:
			Verify existance of the instance in the database.
			If the provided current password matches the one in the database, t an upgrade of the activity state has been successful, proceed to set new values for the password and the private_keyring.
			Otherwise : rollback the session and proceed to return False

		Returns: True/False : bool.

		Exceptions:
			KeyError - raised when the provided payload doesn't consist of two keys.
			ValueErrors - raised when the each nested payload doesn't contain required keys or the values are not of excepted types.
			In case of an arising exception , related to the incorrect assignment , perform the session rollback.
		'''

		assert len(payload)==2, KeyError('The reset requires the payload to consist of only two keys.')
		assert all(map(lambda key: (value:=payload.get(key,None)) is not None and isinstance(value,dict),('password','private_key'))), ValueError('Payload shall contain keys: password:dict and private_key:dict.')
		assert all(map(lambda key: (value:=payload['password'].get(key,None)) is not None and isinstance(value,str),('current','new'))), ValueError('Password shall contain keys: current:str and new:str.')
		assert all(map(lambda key: (value:=payload['private_key'].get(key,None)) is not None and isinstance(value,str),('iv','data'))), ValueError('Private_key shall contain keys: iv:str and data:str.')
		

		if self.__instance is not None and self.__instance.password==payload['password']['current'] and self.update_activity():
			try:
				self.__instance.password=payload['password']['new']
				self.__instance.keyring.private_key=payload['private_key']
				db.session.commit()
				return True
			except:
				db.session.rollback()
		return False


	def update_activity(self):
		'''
		Goal: update the current state of the activity_dnt value.
		[Note this state is related to the security of the tokens , if you wish to learn more about this - view the /utilities/security/validation/headers.py]
		Returns: True if the current inner instance exists , otherwise False. 
		Exceptions:
			In case of an arising exception , related to the database , perform the session rollback.
		'''
		if self.__instance:
			
			try:
				self.__instance.activity_dnt=datetime.fromtimestamp(int(time()))
		
				db.session.commit()
		
				return True
			
			except:
				db.session.rollback()
		
		return False


	def establish_a_chat(self,name):
		'''
		Aimed at the ChatService.
		Goal: create a chat instance , by creating an instance of a ChatService.
		Arguments: identification:int.
		Actions: check if the current user's isinstance exists and create a ChatService instance with provided data.
		If such instance has been successfully created return the ChatService instance 
		Returns: return the instance of the ChatService - If the Actions are all valid and follow the conditions , otherwise - None
		'''
		return (chat if (chat:=service.ChatService()).create(creator_id=self.__instance.id,name=name) else None) if self.__instance else None


	def join_a_chat(self,identification):
		'''
		Aimed at the ChatService.
		Goal: join an existing chat instance , by creating a Participant instance using the ParticipantService.
		Arguments: identification:int.
		Actions: check if the current user's isinstance exists, verify the existance of the chat with such id , after that check if the current user is not a participant of the chat, thus verifying the absence of any related participation.
		Then create a Participation instance using the ParticipationService.
		Returns: True - If the Actions are all valid and follow the conditions , otherwise - False
		Exceptions:
			Raises:
				ValueError - if the data type of the identification is not an integer.
		'''
		
		assert isinstance(identification,int), ValueError('Chat identification shall be an integer.')
		return True if self.__instance and (chat:=service.ChatService(id=identification)).id==identification and (not self in chat) and (participation:=service.ParticipationService()).create(participant_id=self.__instance.id,chat_id=identification) else False

	def discharge_a_chat(self,identification):
		'''
		Aimed at the ChatService.
		Goal: deletes a chat, where the current user is a participant.
		Arguments: identification:int.
		Actions: check if the current user's isinstance exists, then verify if the current user is a participant of the chat and perform the remove process using the ChatService.
		Returns: True - If the Actions are all valid and follow the conditions , otherwise - False
		Exceptions:
			Raises:
				ValueError - if the data type of the identification is not an integer.
		'''
				
		assert isinstance(identification,int), ValueError('Chat identification shall be an integer.')

		return True if self.__instance and (chat:=self.get_a_chat(identification)) and chat.remove() else False
		

	def establish_a_message(self,**payload):
		'''
		Aimed at the MessageService.
		Goal: stores a message istance using the MessageService .
		Arguments: payload:a key word argument = dict : { chat_id:int , content:dict } .
		Actions: check if the current user's isinstance exists, verify if the current user is a participant of the chat.
		Then create a Message instance using the MessageService.
		Returns: message:MessageService - If the Actions are all valid and follow the conditions , otherwise - None
		Exceptions:
			Raises:
				ValueError - if the payload doesn't contain/follow the structure : chat_id:<int> , content:<dict>.
		'''
		assert len(payload)==2 and all(map(lambda key:key in payload and isinstance(payload[key],(int if key=='chat_id' else dict)) ,('chat_id','content'))), ValueError('The payload must contain keys for "chat_id":<int> , "content":<dict>.')
		return message if self.__instance and (chat:=self.get_a_chat(payload['chat_id'])) and (message:=service.MessageService()).create(chat_id=chat.id,sender_id=self.__instance.id,content=payload['content']) else None


	def discharge_a_message(self,**payload):
		'''
		Aimed at the MessageService.
		Goal: removes a message from the chat, where the current user is a participant, using the MessageService.
		Arguments: payload:a key word argument : { chat_id:int , message_id:int } .
		Actions: check if the current user's isinstance exists, then verify if the current user is a participant of the chat, and make sure that the message is in the chat - by using the overriden contains method of the ChatService class.
		Finally, perform the remove process using the MessageService and for the follow up refresh the inner chat and self instance.
		Returns: True - If the Actions are all valid and follow the conditions , otherwise - False
		Exceptions:
			Raises:
				ValueError - if the data type of the identification is not an integer.
		'''
		assert len(payload)==2 and all(map(lambda key:key in payload and isinstance(payload[key],int) ,('chat_id','message_id'))), ValueError('The payload must contain keys for "chat_id":<int> , "message_id":<int>.')
		
		return True if self.__instance and (chat:=self.get_a_chat(payload['chat_id'])) and (message:=service.MessageService(id=payload['message_id'])).id and (message in chat) and message.remove() else False



	def get_a_chat(self,identification):
		'''
		Aimed at the ChatService.
		Goal: return a ChatService instance.
		Arguments: identification:int.
		Actions:if the current user's instance exists, then try to find a participation with a chat_id = <identification>. If there is such a participation establish a ChatService with an id of provided identification.
		Returns: ChatService(id=<identification>) if the current user is in the chat with an id = <identification>.
		Exceptions:
			Raises:
				TypeError - if the data type of the identification is not an integer.
		'''
		
		assert isinstance(identification,int), TypeError('Chat identification shall be an integer.')
		return service.ChatService(id=participation.chat_id) if self.__instance and (participation:=self.__instance.participations.filter_by(chat_id=identification).first())  else None


	def common_ground_with(self,**identification):
		'''
		Aimed at the ChatService,ParticipationService.
		Goal: find a/bunch of common chat/chats.
		Arguments: identification:key-word-argument.
		Actions: if the current user's instance and the other user exists , based on the provided identification. Get the tuple of that user's chat ids, and using it as a base filter the current user's chats, where the chat.id has to be in the pther_chat+ids.
		Returns:tuple(ChatServices, in which both of the users are mentioned as participants)|None
		Exceptions:
			Raises:
				TypeError - if the data type of the identification is not an integer.
		'''
		
		resolve_data_type=lambda key: int if key == 'id' else str

		assert len(identification)==1, SyntaxError('The identification of the other user may accept only 1 unique key at a time.')
		assert any(map(lambda key: key in identification, ('id','email','username'))) , KeyError('The identification payload doesn\'t correspond to any of the unique keys or the datatype is invalid.')


		if self.__instance and (other:=UserService(**identification)).id:
			return tuple(filter(lambda chat: other in chat,self.chats)) if self.__instance else None
		return None


	
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
	def activity_state(self):
		'''
		Goal: retreive the inner "activity state" of the current user.
		[Note: activity state - a timestamped value of the activity_dnt value]
		Returns: activity state:int if inner instance exists Otherwise None
		'''
		return int(datetime.timestamp(self.__instance.activity_dnt)) if self.__instance else None
	

	@property
	def keyring(self):
		'''
		Aimed at the KeyringService.
		Goal: return a KeyringService of the current user.
		Returns: KeyringService instance if inner instance exists Othewise None
		'''
		return service.KeyringService(owner_id=self.__instance.id) if self.__instance else None


	@property
	def chats(self):
		'''
		Aimed at the ChatService.
		Goal: return a sorted list of ChatServices for every participation of the current user , based on the date n time of the activity.
		Returns:a sorted list of ChatServices(id=participation.chat.id) for every participation of the current user if the current user is in the chat with an id = <identification>.
		'''
		return sorted(tuple(service.ChatService(id=participation.chat.id) for participation in self.__instance.participations.all()),key=lambda chat:chat.activity_dnt,reverse=True) if self.__instance else None
	


	@staticmethod
	def __identify(**payload):
		'''
		Goal: Identifies a user based on the given unique payload.
		Arguments: payload is a key word argument, that's used to filter the Keyring table.
		Returns: Instance of the User class / None.
		Exceptions:
			SyntaxError - raised when the payload doesn't contain only one identification key.
			KeyError - raised when the identification key is not appropriate according to the Table constaints.
		'''

		resolve_data_type=lambda key: int if key == 'id' else str

		assert len(payload)==1, SyntaxError('The initialization of the instance may accept only 1 identification at a time.')
		assert any(map(lambda key: key in payload and isinstance(payload[key],resolve_data_type(key)), ('id','email','username'))) , KeyError('The identification payload doesn\'t correspond to any of the unique keys or the datatype is invalid.')

		return User.query.filter_by(**payload).first()


	@staticmethod
	def get(**query):
		'''
		Goal: Query the User table to find a user/users , using the like statement.
		Arguments: query - a key word argument, expecting keys: "name"/"username".
		Lambda functions:
			filter_query:
				Goal: prepare a proper payload for the inside of the filter_query.
				Arguments: payload:key-word-argument, takes in the initial query argument
				Actions: 
					Iterate through each key in the payload with a map:
							If there is a column with such a key return a "sql like" execution for (%[value related to the column]%)
							Otherwise return None
					Then tuple the result.
				Returs: tuple of elements:sql_like_statement|None
		Actions:
			Parse the submited query , using the filter_query , which would return a required tuple of sql like statements for the established columns - the subqueris.
			Then filter the subqueries for the existing ones - not None ones. 
			If there is no subqueries - return None.
			Otherwise execute the filter statement , searching for the values that fit either statement from the parsed_query , and for each of the found users create a UserService with the id of the user , and pack it into a tuple.
			Return a tuple of the UserService instances.
		Returns:tuple(of UserService instances)|None

		Exceptions:
			ValueError - raised when the payload doesn't contain any key related to the unique columns
		'''
		assert any(filter(lambda key: key in query and isinstance(query[key],str),('name','username'))), ValueError('The query payload may only consist of a name and a username parameter.')

		filter_query = lambda payload : tuple( map ( lambda key: column.like(f'%{payload[key]}%') if (column:=User.__dict__.get(key,None)) is not None else column , payload) )

		return tuple(UserService(id=user.id) for user in User.query.filter(db.or_(*parsed_query)).all()) if (parsed_query:=tuple(filter(lambda subquery: subquery is not None,filter_query(query)))) else None


		