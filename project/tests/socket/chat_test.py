from chathouse.utilities.security.token import Token
from chathouse.service import UserService
from flask import current_app
from chathouse.socket import socket
from tests.base import BaseTestCase
import time

class ChatTestCase(BaseTestCase):

	'''
	ChatTestCase - class aimed at testing different requests aimed at the Socket Namespace : /socket/chat.
	'''

	def setUp(self):
		'''
		Goal: set up necessary instance attributes - during every test:
			access_token:lambda function - generates a Token instance , meant to be used as a access token.
				Parameters:update - key word argument - meant to store data required for the access tokens , according to established guidelines - activity and user_id.
				Returns: Token instance
			dummy_identification_paylaod:dict - a dictionary which shall contain identification payloads for the actions , such as : signup or login.
		Returns: None
		'''
		self.access_token = lambda **update: Token(payload_data={'token_type':'access','exp':current_app.config['ACCESS_EXP'],**update})
		
		self.dummy_identification_payload=(
			{
				'signup':{
					'email':'chathousetestclient0@gmail.com',
					'username':'test_username0',
					'name':'Testname0',
					'about':'test_about'
				},
				'login':{
					'identification':'test_username1'
				}
			},
			{
			'signup':{
					'email':'chathousetestclient1@gmail.com',
					'username':'test_username1',
					'name':'Testname1',
					'about':'test_about'
				},
				'login':{
					'identification':'test_username1'
				}
			}
		)

		self.dummy_message_payload={
			'content':{
				'iv':'some intitializing vector',
				'data':'encrypted message data'
				}
		}

		self.namespace='/socket/chat'

		self.socket=socket
		self.socket.init_app(self.app)



	def prepare_user(self,index=0):
		'''
		Goal: prepare a user service instance - by creating one.
		Returns user:UserInstance
		Exceptions:
			Raises:
				ValueError:
					"Coudn't prepare a test user." is caught in cases when one tries to create a user, which already exists -> excepted with a discharge of a user and a resubmission.
					"Still cound't preare a test user." - raised when the discharge,resubmission hasn't helped.

		'''
		user=UserService()
		payload={
			'user_data':{
				'password':'9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
				**self.dummy_identification_payload[index%2]['signup']
			},
			'key_data':{
				'public_key':5,
				'private_key':{'iv':'str','data':'str'}
			}
		}

		try:
			assert user.signup(**payload), ValueError('Couldn\'t prepare a test user.')
		except:
			self.discharge_user(index)
			assert user.signup(**payload), ValueError('Still couldn\'t prepare a test user.')

		return user

	def discharge_user(self,index=0):
		'''
		Goal: remove/delete a test user instance.
		Returns:None
		Exceptions:
			Raises:
				ValueError - in cases,when one tries to discharge a user instance, which is not related to any user. 
		'''
		user=UserService(username=f'test_username{index%2}')
		assert user.remove(), ValueError('Coudn\'t find a test user to remove.')

	#Connect
	def test_valid_connect(self):
		'''
		Goal: test a valid connection call - which performs a "handshake", with necessary data, such as : chat identification, authorized credentials - access token.
		'''
		user = self.prepare_user()

		#Prepare a chat
		chat_id=user.establish_a_chat('A test conversation chat').id
		#Prepare a participation
		user.join_a_chat(chat_id)

		access_token = self.access_token(activity=user.activity_state,user_id=user.id)

		#Estalish a connection for a client
		client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat_id}')

		self.assertTrue(client.is_connected(self.namespace))

		self.discharge_user()

	def test_invalid_connect_unauthorized_invalid_participation(self):
		'''
		Goal: test an invalid connection call - lack of valid participation - a connection to a chat , of which the one making the call is not a participant .
		'''
		user = self.prepare_user()
		other = self.prepare_user(1)
		#Prepare a chat
		chat_id=user.establish_a_chat('A test conversation chat').id
		#Prepare a participation
		user.join_a_chat(chat_id)

		access_token = self.access_token(activity=other.activity_state,user_id=other.id)

		#Tries to establish a connection to a certain chat,where the client is not stated as a participang
		client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat_id}')

		self.assertFalse(client.is_connected(self.namespace))

		self.discharge_user()

	def test_invalid_connect_unauthorized_expired_token(self):
		'''
		Goal: test an invalid connection call - expired access token.
		'''
		user = self.prepare_user()
		#Prepare a chat
		chat_id=user.establish_a_chat('A test conversation chat').id
		#Prepare a participation
		user.join_a_chat(chat_id)

		access_token = self.access_token(activity=user.activity_state,user_id=user.id,exp={'seconds':1})

		time.sleep(2)

		#Tries to establish a connection to a certain chat,where the client is not stated as a participang
		client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat_id}')

		self.assertFalse(client.is_connected(self.namespace))

		self.discharge_user()

	def test_invalid_connect_unauthorized_invalid_activity_state(self):
		'''
		Goal: test an invalid connection call - invalid assigned state value in the access token - ie the user has logged out.
		'''
		user = self.prepare_user()
		#Prepare a chat
		chat_id=user.establish_a_chat('A test conversation chat').id
		#Prepare a participation
		user.join_a_chat(chat_id)

		access_token = self.access_token(activity=user.activity_state,user_id=user.id)

		time.sleep(1)
		user.update_activity()

		#Tries to establish a connection to a certain chat,where the client is not stated as a participang
		client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat_id}')

		self.assertFalse(client.is_connected(self.namespace))

		self.discharge_user()

	def test_invalid_connect_unauthorized_absent_query(self):
		'''
		Goal: test an invalid connection call - absence of the chat_id parameter.
		'''
		user = self.prepare_user()
		#Prepare a chat
		chat_id=user.establish_a_chat('A test conversation chat').id
		#Prepare a participation
		user.join_a_chat(chat_id)

		access_token = self.access_token(activity=user.activity_state,user_id=user.id)

		time.sleep(1)
		user.update_activity()

		#Tries to establish a connection to a certain chat,where the client is not stated as a participang
		client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})

		self.assertFalse(client.is_connected(self.namespace))

		self.discharge_user()

	def test_invalid_connect_unauthorized_invalid_query(self):
		'''
		Goal: test an invalid connection call - invalid chat_id parameter.
		'''
		user = self.prepare_user()
		#Prepare a chat
		chat_id=user.establish_a_chat('A test conversation chat').id
		#Prepare a participation
		user.join_a_chat(chat_id)

		access_token = self.access_token(activity=user.activity_state,user_id=user.id)

		time.sleep(1)
		user.update_activity()

		#Tries to establish a connection to a certain chat,where the client is not stated as a participang
		client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string='dummy')

		self.assertFalse(client.is_connected(self.namespace))

		self.discharge_user()

	#Establish a message
	def test_valid_establish_a_message(self):
		'''
		Goal: test a valid establish a message call - which creates a message relating it to a chat.
		Actions:
			1.Prepare users.
			2.Prepare a chat and participations.
			3.Set up connections to their respective notification namespaces and connect to a common chat namespace.
			4.Verify the connections.
			5.Either user establishes a message /w dummy payload.
			6.Verify the callbacks for namespaces:
				Notification :
					1)The response is a non empty list;
					2)The name of the callback is "established_message";
					3)The response contains args , which is a non empty list with a first element - a dictionary;
					4)The dictionary in the args contains an id;
					5)The content and sender values shall be the ones , which have been provided at the first place.
				Chat:
					1)The response is a non empty list;
					2)The name of the callback is "established_message";
					3)The response contains args , which is a non empty list with a first element - a dictionary;
					4)The dictionary in the args contains an id;
					5)The chat id and chat name values shall be the ones , that are related to the established chat.
		'''
		notification_namespace='/socket/notification'
		#Prepare users - future participants
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)
		#Prepare a chat
		chat=current_user.establish_a_chat('A test conversation chat')
		#Prepare a participation
		current_user.join_a_chat(chat.id)
		other_user.join_a_chat(chat.id)

		#Prepare an access token for the "current" user
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		#Connect to a notification namespace with the respective access token
		current_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat namespace , providing the respective access token
		current_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')
		
		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(current_client_notification.is_connected(notification_namespace))
		self.assertTrue(current_client_chat.is_connected(self.namespace))

		#Prepare an access token for the "other" user
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id)
		#Connect to a notification socket with the respective access token
		other_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat socket , providing the respective access token
		other_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')

		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(other_client_notification.is_connected(notification_namespace))
		self.assertTrue(other_client_chat.is_connected(self.namespace))

		#Either participant establishes an encrypted message with proper payload

		current_client_chat.emit('establish_a_message',self.dummy_message_payload,namespace=self.namespace,to=chat.id)

		message_assert = lambda response,expected: (a for a in (\
			self.assertIsInstance(response,list),\
			self.assertTrue(len(response)>0),\
			self.assertEqual('established_message',response[0].get('name','')),\
			self.assertIsInstance(response[0].get('args',None),list),\
			self.assertTrue(len(response[0]['args'])>0 and isinstance(response[0]['args'][0],dict) ),\
			self.assertIn('id',response[0]['args'][0]),\
			self.assertEqual(expected['content'],response[0]['args'][0].get('content',None)),\
			self.assertEqual(expected['sender'],response[0]['args'][0].get('sender',None)),\
			))

		notification_assert = lambda response,expected: (a for a in (\
			self.assertIsInstance(response,list),\
			self.assertTrue(len(response)>0),\
			self.assertEqual('chat_activity',response[0].get('name','')),\
			self.assertIsInstance(response[0].get('args',None),list),\
			self.assertTrue(len(response[0]['args'])>0 and isinstance(response[0]['args'][0],dict) ),\
			self.assertEqual(expected['id'],response[0]['args'][0].get('id',None)),\
			self.assertEqual(expected['name'],response[0]['args'][0].get('name',None)),\
			))

		notification_assert(current_client_notification.get_received(notification_namespace),{'id':chat.id,'name':chat.name})
		notification_assert(other_client_notification.get_received(notification_namespace),{'id':chat.id,'name':chat.name})

		message_assert(current_client_chat.get_received(self.namespace),{**self.dummy_message_payload,'sender':{'id':current_user.id,'username':current_user.username} })
		message_assert(other_client_chat.get_received(self.namespace),{**self.dummy_message_payload,'sender':{'id':current_user.id,'username':current_user.username} })


		self.discharge_user()
		self.discharge_user(1)

	def test_invalid_establish_a_message_chat_gone(self):
		'''
		Goal: test an invalid establish a message call. Invalid according to the improper authorization - chat is gone.
		Actions:
			1.Prepare users.
			2.Prepare a chat and participations.
			3.Set up connections to their respective notification namespaces and connect to a common chat namespace.
			4.Verify the connections.
			5.The creator discharges their account - thus the chat is removed as well
			6.The other participant tries to establish a message /w dummy payload.
			7.The call must result in a disconnect.
		'''
		notification_namespace='/socket/notification'
		#Prepare users - future participants
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)
		#Prepare a chat
		chat=current_user.establish_a_chat('A test conversation chat')
		#Prepare a participation
		current_user.join_a_chat(chat.id)
		other_user.join_a_chat(chat.id)

		#Prepare an access token for the "current" user
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		#Connect to a notification namespace with the respective access token
		current_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat namespace , providing the respective access token
		current_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')
		
		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(current_client_notification.is_connected(notification_namespace))
		self.assertTrue(current_client_chat.is_connected(self.namespace))

		#Prepare an access token for the "other" user
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id)
		#Connect to a notification socket with the respective access token
		other_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat socket , providing the respective access token
		other_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')

		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(other_client_notification.is_connected(notification_namespace))
		self.assertTrue(other_client_chat.is_connected(self.namespace))

		#The creator of the chat - has discharged their account - the chat has been removed also
		current_user.remove()

		#Either participant establishes an encrypted message with proper payload
		other_client_chat.emit('establish_a_message',self.dummy_message_payload,namespace=self.namespace,to=chat.id)
		
		#The establishing must result in a disconnect - due to unauthorized call aimed at a chat , that no longer exists
		self.assertFalse(other_client_chat.is_connected(self.namespace))
		
		other_user.remove()

	def test_invalid_establish_a_message_unauthorized_access_token_expired(self):
		'''
		Goal: test an invalid establish a message call. Invalid according to the improper authorization - access token has expired - thus the emit caused a disconnect.
		Actions:
			1.Prepare users.
			2.Prepare a chat and participations.
			3.Set up connections to their respective notification namespaces and connect to a common chat namespace.
			4.Verify the connections.
			5.Either participant tries to establish a new message - let it be the other one.
			6.The call must result in a disconnect.
		'''
		notification_namespace='/socket/notification'
		#Prepare users - future participants
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)
		#Prepare a chat
		chat=current_user.establish_a_chat('A test conversation chat')
		#Prepare a participation
		current_user.join_a_chat(chat.id)
		other_user.join_a_chat(chat.id)

		message=current_user.establish_a_message(chat_id=chat.id,**self.dummy_message_payload)
		
		#Prepare an access token for the "current" user
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		#Connect to a notification namespace with the respective access token
		current_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat namespace , providing the respective access token
		current_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')
		
		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(current_client_notification.is_connected(notification_namespace))
		self.assertTrue(current_client_chat.is_connected(self.namespace))

		#Prepare an access token for the "other" user
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id,exp={'seconds':1})
		#Connect to a notification socket with the respective access token
		other_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat socket , providing the respective access token
		other_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')

		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(other_client_notification.is_connected(notification_namespace))
		self.assertTrue(other_client_chat.is_connected(self.namespace))

		time.sleep(2)

		#Either participant discharges mesaages/a message - providing a message id, related to the chat
		other_client_chat.emit('establish_a_message',self.dummy_message_payload,namespace=self.namespace,to=chat.id)

		#The discharging must result in a disconnect - due to unauthorized call aimed at a chat , that no longer exists
		self.assertFalse(other_client_chat.is_connected(self.namespace))
		
		other_user.remove()

	def test_invalid_establish_a_message_payload_invalid_datatype(self):
		'''
		Goal: test an invalid establish a message call. Invalid according to the improper payload - datatype.
		Actions:
			1.Prepare users.
			2.Prepare a chat and participations.
			3.Set up connections to their respective notification namespaces and connect to a common chat namespace.
			4.Verify the connections.
			5.Either user establishes a message /w a payload , which contains a value of invalid datatype.
			6.Verify the callbacks for namespaces:
				Notification :
					1)The response is a non empty list;
					2)The name of the callback is "error";
					3)The response contains args , which is a non empty list with a first element - a dictionary;
					4)The error message shall be "Please submit a valid payload." .
		'''
		notification_namespace='/socket/notification'
		#Prepare users - future participants
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)
		#Prepare a chat
		chat=current_user.establish_a_chat('A test conversation chat')
		#Prepare a participation
		current_user.join_a_chat(chat.id)
		other_user.join_a_chat(chat.id)

		#Prepare an access token for the "current" user
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		#Connect to a notification namespace with the respective access token
		current_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat namespace , providing the respective access token
		current_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')
		
		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(current_client_notification.is_connected(notification_namespace))
		self.assertTrue(current_client_chat.is_connected(self.namespace))

		#Prepare an access token for the "other" user
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id)
		#Connect to a notification socket with the respective access token
		other_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat socket , providing the respective access token
		other_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')

		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(other_client_notification.is_connected(notification_namespace))
		self.assertTrue(other_client_chat.is_connected(self.namespace))

		#Either participant establishes an encrypted message with proper payload
		current_client_chat.emit('establish_a_message',{'content':{'iv':'str','data':1}},namespace=self.namespace,to=chat.id)
		
		notification_assert = lambda response,expected: (a for a in (\
			self.assertIsInstance(response,list),\
			self.assertTrue(len(response)>0),\
			self.assertEqual('error',response[0].get('name','')),\
			self.assertIsInstance(response[0].get('args',None),list),\
			self.assertTrue(len(response[0]['args'])>0 and isinstance(response[0]['args'][0],dict) ),\
			self.assertEqual(expected['message'],response[0]['args'][0].get('message',None)),\
			))

		notification_assert(current_client_notification.get_received(notification_namespace),{'message':'Please submit a valid payload.'})
		
		self.discharge_user()
		self.discharge_user(1)

	def test_invalid_establish_a_message_payload_invalid_keys(self):
		'''
		Goal: test an invalid establish a message call. Invalid according to the improper payload - unexpected key.
		Actions:
			1.Prepare users.
			2.Prepare a chat and participations.
			3.Set up connections to their respective notification namespaces and connect to a common chat namespace.
			4.Verify the connections.
			5.Either user establishes a message /w a payload , which contains a value of invalid datatype.
			6.Verify the callbacks for namespaces:
				Notification :
					1)The response is a non empty list;
					2)The name of the callback is "error";
					3)The response contains args , which is a non empty list with a first element - a dictionary;
					4)The error message shall be "Please submit a valid payload." .
		'''
		notification_namespace='/socket/notification'
		#Prepare users - future participants
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)
		#Prepare a chat
		chat=current_user.establish_a_chat('A test conversation chat')
		#Prepare a participation
		current_user.join_a_chat(chat.id)
		other_user.join_a_chat(chat.id)

		#Prepare an access token for the "current" user
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		#Connect to a notification namespace with the respective access token
		current_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat namespace , providing the respective access token
		current_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')
		
		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(current_client_notification.is_connected(notification_namespace))
		self.assertTrue(current_client_chat.is_connected(self.namespace))

		#Prepare an access token for the "other" user
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id)
		#Connect to a notification socket with the respective access token
		other_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat socket , providing the respective access token
		other_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')

		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(other_client_notification.is_connected(notification_namespace))
		self.assertTrue(other_client_chat.is_connected(self.namespace))

		#Either participant establishes an encrypted message with proper payload
		current_client_chat.emit('establish_a_message',{'content':{'iv':'string','data':'string'},'new_key':'some value'},namespace=self.namespace,to=chat.id)
		
		notification_assert = lambda response,expected: (a for a in (\
			self.assertIsInstance(response,list),\
			self.assertTrue(len(response)>0),\
			self.assertEqual('error',response[0].get('name','')),\
			self.assertIsInstance(response[0].get('args',None),list),\
			self.assertTrue(len(response[0]['args'])>0 and isinstance(response[0]['args'][0],dict) ),\
			self.assertEqual(expected['message'],response[0]['args'][0].get('message',None)),\
			))

		notification_assert(current_client_notification.get_received(notification_namespace),{'message':'Please submit a valid payload.'})
		
		self.discharge_user()
		self.discharge_user(1)

	#Discharge a message
	def test_valid_discharge_messages(self):
		'''
		Goal: test a valid discharge messages call - which removes provided message ids , related to a chat.
		Actions:
			1.Prepare users.
			2.Prepare a chat,participations and a message /w dummy payload.
			3.Set up connections to their respective notification namespaces and connect to a common chat namespace.
			4.Verify the connections.
			5.Either user discharges a message /w an id.
			6.Verify the callbacks for namespaces:
				Notification :
					1)The response is a non empty list;
					2)The name of the callback is "established_message";
					3)The response contains args , which is a non empty list with a first element - a dictionary;
					4)The dictionary in the args contains an id;
					5)The content and sender values shall be the ones , which have been provided at the first place.
				Chat:
					1)The response is a non empty list;
					2)The name of the callback is "established_message";
					3)The response contains args , which is a non empty list with a first element - a dictionary;
					4)The ids in the messages list shall be the ones , which have been provided at the first place.
		'''
		notification_namespace='/socket/notification'
		#Prepare users - future participants
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)
		#Prepare a chat
		chat=current_user.establish_a_chat('A test conversation chat')
		#Prepare a participation
		current_user.join_a_chat(chat.id)
		other_user.join_a_chat(chat.id)

		message=current_user.establish_a_message(chat_id=chat.id,**self.dummy_message_payload)
		
		#Prepare an access token for the "current" user
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		#Connect to a notification namespace with the respective access token
		current_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat namespace , providing the respective access token
		current_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')
		
		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(current_client_notification.is_connected(notification_namespace))
		self.assertTrue(current_client_chat.is_connected(self.namespace))

		#Prepare an access token for the "other" user
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id)
		#Connect to a notification socket with the respective access token
		other_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat socket , providing the respective access token
		other_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')

		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(other_client_notification.is_connected(notification_namespace))
		self.assertTrue(other_client_chat.is_connected(self.namespace))

		#Either participant discharges mesaages/a message - providing a message id, related to the chat

		other_client_chat.emit('discharge_messages',{'messages':[message.id]},namespace=self.namespace,to=chat.id)

		message_assert = lambda response,expected: (a for a in (\
			self.assertIsInstance(response,list),\
			self.assertTrue(len(response)>0),\
			self.assertEqual('discharged_messages',response[0].get('name','')),\
			self.assertIsInstance(response[0].get('args',None),list),\
			self.assertTrue(len(response[0]['args'])>0 and isinstance(response[0]['args'][0],dict) ),\
			self.assertEqual(expected['messages'],response[0]['args'][0].get('messages',None)),\
			))

		notification_assert = lambda response,expected: (a for a in (\
			self.assertIsInstance(response,list),\
			self.assertTrue(len(response)>0),\
			self.assertEqual('chat_activity',response[0].get('name','')),\
			self.assertIsInstance(response[0].get('args',None),list),\
			self.assertTrue(len(response[0]['args'])>0 and isinstance(response[0]['args'][0],dict) ),\
			self.assertEqual(expected['id'],response[0]['args'][0].get('id',None)),\
			self.assertEqual(expected['name'],response[0]['args'][0].get('name',None)),\
			))

		notification_assert(current_client_notification.get_received(notification_namespace),{'id':chat.id,'name':chat.name})
		notification_assert(other_client_notification.get_received(notification_namespace),{'id':chat.id,'name':chat.name})

		message_assert(current_client_chat.get_received(self.namespace),{'messages':[message.id]})
		message_assert(other_client_chat.get_received(self.namespace),{'messages':[message.id]})


		self.discharge_user()
		self.discharge_user(1)

	def test_invalid_discharge_messages_chat_gone(self):
		'''
		Goal: test an invalid discharge messages call. Invalid according to the improper authorization - chat is gone.
		Actions:
			1.Prepare users.
			2.Prepare a chat,participations and a dummy message.
			3.Set up connections to their respective notification namespaces and connect to a common chat namespace.
			4.Verify the connections.
			5.The creator discharges their account - thus the chat is removed as well
			6.The other participant tries to discharge the previously created message.
			7.The call must result in a disconnect.
		'''
		notification_namespace='/socket/notification'
		#Prepare users - future participants
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)
		#Prepare a chat
		chat=current_user.establish_a_chat('A test conversation chat')
		#Prepare a participation
		current_user.join_a_chat(chat.id)
		other_user.join_a_chat(chat.id)

		message=current_user.establish_a_message(chat_id=chat.id,**self.dummy_message_payload)
		
		#Prepare an access token for the "current" user
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		#Connect to a notification namespace with the respective access token
		current_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat namespace , providing the respective access token
		current_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')
		
		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(current_client_notification.is_connected(notification_namespace))
		self.assertTrue(current_client_chat.is_connected(self.namespace))

		#Prepare an access token for the "other" user
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id)
		#Connect to a notification socket with the respective access token
		other_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat socket , providing the respective access token
		other_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')

		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(other_client_notification.is_connected(notification_namespace))
		self.assertTrue(other_client_chat.is_connected(self.namespace))

		#The creator of the chat - has discharged their account - the chat has been removed also
		current_user.remove()

		#Either participant discharges mesaages/a message - providing a message id, related to the chat
		other_client_chat.emit('discharge_messages',{'messages':[message.id]},namespace=self.namespace,to=chat.id)

		#The discharging must result in a disconnect - due to unauthorized call aimed at a chat , that no longer exists
		self.assertFalse(other_client_chat.is_connected(self.namespace))
		
		other_user.remove()

	def test_invalid_discharge_messages_unauthorized_access_token_expired(self):
		'''
		Goal: test an invalid discharge messages call. Invalid according to the improper authorization - access token has expired - thus the emit caused a disconnect.
		Actions:
			1.Prepare users.
			2.Prepare a chat and participations.
			3.Set up connections to their respective notification namespaces and connect to a common chat namespace.
			4.Verify the connections.
			5.Either participant tries to discharge the previously created message - let it be the other one.
			6.The call must result in a disconnect.
		'''
		notification_namespace='/socket/notification'
		#Prepare users - future participants
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)
		#Prepare a chat
		chat=current_user.establish_a_chat('A test conversation chat')
		#Prepare a participation
		current_user.join_a_chat(chat.id)
		other_user.join_a_chat(chat.id)

		message=current_user.establish_a_message(chat_id=chat.id,**self.dummy_message_payload)
		
		#Prepare an access token for the "current" user
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		#Connect to a notification namespace with the respective access token
		current_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat namespace , providing the respective access token
		current_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')
		
		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(current_client_notification.is_connected(notification_namespace))
		self.assertTrue(current_client_chat.is_connected(self.namespace))

		#Prepare an access token for the "other" user
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id,exp={'seconds':1})
		#Connect to a notification socket with the respective access token
		other_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat socket , providing the respective access token
		other_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')

		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(other_client_notification.is_connected(notification_namespace))
		self.assertTrue(other_client_chat.is_connected(self.namespace))

		time.sleep(2)

		#Either participant discharges mesaages/a message - providing a message id, related to the chat
		other_client_chat.emit('discharge_messages',{'messages':[message.id]},namespace=self.namespace,to=chat.id)

		#The discharging must result in a disconnect - due to unauthorized call aimed at a chat , that no longer exists
		self.assertFalse(other_client_chat.is_connected(self.namespace))
		
		other_user.remove()

	def test_invalid_discharge_messages_payload_invalid_datatype(self):
		'''
		Goal: test an invalid establish a message call. Invalid according to the improper payload - datatype of the "message" value.
		Actions:
			1.Prepare users.
			2.Prepare a chat , participations and a dummy message.
			3.Set up connections to their respective notification namespaces and connect to a common chat namespace.
			4.Verify the connections.
			5.Either participant tries to discharge the previously created message - let it be the other one.
			6.Verify the callbacks for namespaces:
				Notification :
					1)The response is a non empty list;
					2)The name of the callback is "error";
					3)The response contains args , which is a non empty list with a first element - a dictionary;
					4)The error message shall be "Please submit a valid payload." .
		'''
		notification_namespace='/socket/notification'
		#Prepare users - future participants
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)
		#Prepare a chat
		chat=current_user.establish_a_chat('A test conversation chat')
		#Prepare a participation
		current_user.join_a_chat(chat.id)
		other_user.join_a_chat(chat.id)

		message=current_user.establish_a_message(chat_id=chat.id,**self.dummy_message_payload)
		
		#Prepare an access token for the "current" user
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		#Connect to a notification namespace with the respective access token
		current_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat namespace , providing the respective access token
		current_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')
		
		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(current_client_notification.is_connected(notification_namespace))
		self.assertTrue(current_client_chat.is_connected(self.namespace))

		#Prepare an access token for the "other" user
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id)
		#Connect to a notification socket with the respective access token
		other_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat socket , providing the respective access token
		other_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')

		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(other_client_notification.is_connected(notification_namespace))
		self.assertTrue(other_client_chat.is_connected(self.namespace))

		#Either participant discharges mesaages/a message - providing a message id, related to the chat
		other_client_chat.emit('discharge_messages',{'messages':message.id},namespace=self.namespace,to=chat.id)
		
		notification_assert = lambda response,expected: (a for a in (\
			self.assertIsInstance(response,list),\
			self.assertTrue(len(response)>0),\
			self.assertEqual('error',response[0].get('name','')),\
			self.assertIsInstance(response[0].get('args',None),list),\
			self.assertTrue(len(response[0]['args'])>0 and isinstance(response[0]['args'][0],dict) ),\
			self.assertEqual(expected['message'],response[0]['args'][0].get('message',None)),\
			))

		notification_assert(other_client_notification.get_received(notification_namespace),{'message':'Invalid payload.'})
		
		self.discharge_user()
		self.discharge_user(1)

	def test_invalid_discharge_messages_payload_invalid_inner_datatype(self):
		'''
		Goal: test an invalid establish a message call. Invalid according to the improper payload - inner datatype of values/a value.
		Actions:
			1.Prepare users.
			2.Prepare a chat , participations and a dummy message.
			3.Set up connections to their respective notification namespaces and connect to a common chat namespace.
			4.Verify the connections.
			5.Either participant tries to discharge the previously created message - let it be the other one.
			6.Verify the callbacks for namespaces:
				Notification :
					1)The response is a non empty list;
					2)The name of the callback is "error";
					3)The response contains args , which is a non empty list with a first element - a dictionary;
					4)The error message shall be "Please submit a valid payload." .
		'''
		notification_namespace='/socket/notification'
		#Prepare users - future participants
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)
		#Prepare a chat
		chat=current_user.establish_a_chat('A test conversation chat')
		#Prepare a participation
		current_user.join_a_chat(chat.id)
		other_user.join_a_chat(chat.id)

		message=current_user.establish_a_message(chat_id=chat.id,**self.dummy_message_payload)
		
		#Prepare an access token for the "current" user
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		#Connect to a notification namespace with the respective access token
		current_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat namespace , providing the respective access token
		current_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')
		
		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(current_client_notification.is_connected(notification_namespace))
		self.assertTrue(current_client_chat.is_connected(self.namespace))

		#Prepare an access token for the "other" user
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id)
		#Connect to a notification socket with the respective access token
		other_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat socket , providing the respective access token
		other_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')

		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(other_client_notification.is_connected(notification_namespace))
		self.assertTrue(other_client_chat.is_connected(self.namespace))

		#Either participant discharges mesaages/a message - providing a message id, related to the chat
		other_client_chat.emit('discharge_messages',{'messages':[str(message.id)]},namespace=self.namespace,to=chat.id)
		
		notification_assert = lambda response,expected: (a for a in (\
			self.assertIsInstance(response,list),\
			self.assertTrue(len(response)>0),\
			self.assertEqual('error',response[0].get('name','')),\
			self.assertIsInstance(response[0].get('args',None),list),\
			self.assertTrue(len(response[0]['args'])>0 and isinstance(response[0]['args'][0],dict) ),\
			self.assertEqual(expected['message'],response[0]['args'][0].get('message',None)),\
			))

		notification_assert(other_client_notification.get_received(notification_namespace),{'message':'Invalid payload.'})
		
		self.discharge_user()
		self.discharge_user(1)

	def test_invalid_discharge_messages_payload_invalid_message_ids(self):
		'''
		Goal: test an invalid establish a message call. Invalid according to the improper payload - inner datatype of values/a value.
		Actions:
			1.Prepare users.
			2.Prepare a chat , participations and a dummy message.
			3.Set up connections to their respective notification namespaces and connect to a common chat namespace.
			4.Verify the connections.
			5.Either participant tries to discharge the previously created message - let it be the other one.
			6.Verify the callbacks for namespaces:
				Notification :
					1)The response is a non empty list;
					2)The name of the callback is "error";
					3)The response contains args , which is a non empty list with a first element - a dictionary;
					4)The error message shall be "Please submit a valid payload." .
		'''
		notification_namespace='/socket/notification'
		#Prepare users - future participants
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)
		#Prepare a chat
		chat=current_user.establish_a_chat('A test conversation chat')
		#Prepare a participation
		current_user.join_a_chat(chat.id)
		other_user.join_a_chat(chat.id)

		message=current_user.establish_a_message(chat_id=chat.id,**self.dummy_message_payload)

		
		#Prepare an access token for the "current" user
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		#Connect to a notification namespace with the respective access token
		current_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat namespace , providing the respective access token
		current_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')
		
		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(current_client_notification.is_connected(notification_namespace))
		self.assertTrue(current_client_chat.is_connected(self.namespace))

		#Prepare an access token for the "other" user
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id)
		#Connect to a notification socket with the respective access token
		other_client_notification = self.socket.test_client(self.app,namespace=notification_namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		#Connect to a room in the chat socket , providing the respective access token
		other_client_chat = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'},query_string=f'chat_id={chat.id}')

		#Make sure of the connection to the mentioned notification and chat namespaces.
		self.assertTrue(other_client_notification.is_connected(notification_namespace))
		self.assertTrue(other_client_chat.is_connected(self.namespace))

		#Either participant discharges mesaages/a message - providing a message id, related to the chat
		other_client_chat.emit('discharge_messages',{'messages':[message.id,2]},namespace=self.namespace,to=chat.id)
		
		notification_assert = lambda response,expected: (a for a in (\
			self.assertIsInstance(response,list),\
			self.assertTrue(len(response)>0),\
			self.assertEqual('error',response[0].get('name','')),\
			self.assertIsInstance(response[0].get('args',None),list),\
			self.assertTrue(len(response[0]['args'])>0 and isinstance(response[0]['args'][0],dict) ),\
			self.assertEqual(expected['message'],response[0]['args'][0].get('message',None)),\
			))

		notification_assert(other_client_notification.get_received(notification_namespace),{'message':'Invalid payload - not all provided messages have been discharged.'})
		
		self.discharge_user()
		self.discharge_user(1)