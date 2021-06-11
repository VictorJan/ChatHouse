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
		Goal: test an invalid connection call - absense of the chat_id parameter.
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