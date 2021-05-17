from chathouse.models import db,User,Keyring
import chathouse.service as service
from copy import deepcopy

class UserService:
	'''
	The  UserService defines required methods and properties, necessary to perform the Authenticaion,CRUD and other actions.
	'''
	def __init__(self,**identification):
		'''
		Arguments: identification is a key word argument, that shall only include proper unique keys.
		'''
		self.__instance=self.__identify(**identification) if identification else None

	def remove(self):
		'''
		Goal: remove the current instance of the User class.
		Returns: True/False:bool.
		Exceptions:
			In case of an arrising exception , related to delete method, perform the session rollback.
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


	def signup(self,**payload):
		'''
		Goal: perform a signup process for a user , creating an according keyring, a "selfchat" with proper "selfparticipation".
		Chain calls to :  self.join 

		Arguments: payload - a dictionary key word argument , which shall consist of 2 dictionaries: user_data and a key_data.
		Excpecting: user_data:{
			"username":<str>
			"email":<str>
			"name":<str>
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
			In case of an arrising exception , related to the incorrect payload used in the session oparation , perform the session rollback.
		'''

		assert len(payload)==2, Exception('The signup requires the payload to consist of two keys.')
		assert all(map( lambda key: key in payload and isinstance(payload[key],dict), ('user_data','key_data'))) , ValueError('The payload must contain keys for "user_data" and "key_data" , which have to be dictionaries.')

		if self.__instance is None:
			try:
				self.__instance=User(**payload['user_data'])
				db.session.add(self.__instance)
				db.session.flush()

				payload['key_data']['owner_id']=self.__instance.id

				if (keyring:=service.KeyringService(owner_id=payload['key_data']['owner_id'])).create(**payload['key_data']) and (chat:=self.start_a_chat('Saved Messages')) and self.join_a_chat(chat.id):

					db.session.refresh(self.__instance)
					return True

				else:
					db.session.rollback()
					
					if keyring.id is not None:
						chat.remove()
					
					keyring.remove()

					self.__instance=None

					return False
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
			Check if the provided password matches the one in the database, incriment the token_version value : return True.
			Otherwise : rollback the session for the update of the token_ and remove all of the instances : return False

		Returns: True/False : bool.

		Exceptions:
			Exception - raised when the provided payload doesn't consist of one necessary key.
			TypeError - raised when the payload doesn't contain required keys or the values are not of dictionary type.
			In case of an arrising exception , related to the incorrect payload , perform the session rollback.
		'''

		assert len(payload)==1 and payload.get('password'), ValueError('The login requires the payload to consist of only one key - "password".')
		assert isinstance(payload.get('password',None),str) , TyperError('The payload must contain a password key, the value of which must be a string.')

		if self.__instance is not None and self.__instance.password==payload['password']:
			try:
				self.__instance.token_version+=1
				db.session.commit()
				db.session.refresh(self.__instance)
				return True
			except:
				db.session.rollback()
				return False
		return False



	def start_a_chat(self,name):
		'''
		Aimed at the ChatService.
		Goal: create a chat instance , by creating an instance of a ChatService.
		Arguments: identification:int.
		Actions: check if the current user's isinstance exists.
		Returns: return the instance of the ChatService - If the Actions are all valid and return True , otherwise - None
		'''

		return (running_chat if (running_chat:=service.ChatService()).create(creator_id=self.__instance.id,name=name) else None) if self.__instance else None


	def join_a_chat(self,identification):
		'''
		Aimed at the ChatService.
		Goal: join an existing chat instance , by creating a Participant instance using the ParticipantService.
		Arguments: identification:int.
		Actions: check if the current user's isinstance exists, verify the existance of the chat with such id , after that check if the current user is not a participant of the chat, thus verifying the absence of any related participation.
		Then create a Participation istance using the ParticipationService.
		Returns: True - If the Actions are all valid and return True , otherwise - False
		Exceptions:
			Raises:
				ValueError - if the data type of the identification is not an integer.
		'''
		
		assert isinstance(identification,int), ValueError('Chat identification shall be an integer.')

		if self.__instance and self.get_a_chat(identification) is None and (chat:=service.ChatService(id=identification)) and (participation:=service.ParticipationService()).create(participant_id=self.__instance.id,chat_id=chat.id):
				return True
		return False

	def delete_a_chat(self,identification):
		'''
		Aimed at the ChatService.
		Goal: deletes a chat, where the current user is a participant.
		Arguments: identification:int.
		Actions: check if the current user's isinstance exists, then verify if the current user is a participant of the chat and perform the remove process using the ChatService.
		Returns: True - If the Actions are all valid and return True , otherwise - False
		Exceptions:
			Raises:
				ValueError - if the data type of the identification is not an integer.
		'''
				
		assert instance(identification,int), ValueError('Chat identification shall be an integer.')

		if self.__instance and (chat:=self.get_a_chat(identification)) and chat.remove():
			return True
		return False
		

	def create_a_message(self,**payload):
		'''
		Aimed at the MessageService.
		Goal: stores a message istance using the MessageService .
		Arguments: payload:a key word argument = dict : { chat_id:int , content:dict } .
		Actions: check if the current user's isinstance exists, then verify if the current user is a participant of the chat and perform the remove process using the ChatService.
		Returns: True - If the Actions are all valid and return True , otherwise - False
		Exceptions:
			Raises:
				ValueError - if the data type of the identification is not an integer.
		'''
		resolve_data_type=lambda key: int if key == 'chat_id' else dict
		assert len(payload)==2 and all(map(lambda key:key in payload and isinstance(payload[key],(int if key=='chat_id' else dict)) ,('chat_id','content'))), ValueError('The payload must contain keys for "chat_id":<int> , "content":<dict>.')

		if self.__instance and (chat:=self.get_a_chat(payload['chat_id'])) and service.MessageService().create(chat_id=chat.id,sender_id=self.__instance.id,content=payload['content']):
			return True
		return False



	def get_a_chat(self,identification):
		'''
		Aimed at the ChatService.
		Goal: return a ChatService instance.
		Arguments: identification:int.
		Returns: ChatService(id=<identification>) if the current user is in the chat with an id = <identification>.
		Exceptions:
			Raises:
				TypeError - if the data type of the identification is not an integer.
		'''
		
		assert isinstance(identification,int), TypeError('Chat identification shall be an integer.')

		return service.ChatService(id=participation.chat_id) if self.__instance and (participation:=self.__instance.participations.filter_by(chat_id=identification).first())  else None


	def a_chat_with(self,**identification):
		if self.__instance and (other:=UserService(**identification)):
			return None

	
	def __getattr__(self,attr):
		return ( deepcopy(value) if (value:=self.__instance.__dict__.get(attr,None)) is not None else value ) if self.__instance else None


	@property
	def keyring(self):
		return service.KeyringService(owner_id=self.__instance.id) if self.__instance else None


	@property
	def chats(self):
		return [service.ChatService(id=participation.chat.id) for participation in self.__instance.participations.all()] if self.__instance else None
	


	@staticmethod
	def __identify(**payload):
		'''
		Goal: Identifies a user based on the given unique payload.

		Arguments: payload is a key word argument, that's used to filter the Keyring table.
		Returns: Instance of the User class / None.
		Exceptions:
			SyntaxError - raised when the payload doesn't contain only one identification key.
			KeyError - raised when the identification key is not appropriate according to the Table constaints
		'''
		assert len(payload)==1, SyntaxError('The initialization of the instance may accept only 1 identification at a time.')
		assert any(map(lambda key: key in payload, ('id','email','username'))) , KeyError('The identification payload doesn\'t correspond to any of the unique keys.')

		return User.query.filter_by(**payload).first()


	@staticmethod
	def get(**query):
		'''
		Goal: Query the User table to find a user/users , using the like statement.
		Arguments: query - a key word argument, expecting keys: "name"/"username".
		
		'''

		assert any(filter(lambda key: key in query and isinstance(query[key],str),('name,username'))), SyntaxError('The query payload may only consist of a name and a username parameter.')

		filter_query = lambda payload : tuple( map ( lambda key: column.like(f'%{payload[key]}%') if (column:=User.__dict__.get(key,None)) is not None else column , payload) )

		return [UserService(id=user.id) for user in User.query.filter(db.or_(*parsed_query))] if (parsed_query:=tuple(filter(lambda subquery: subquery is not None,filter_query(query)))) else None


		