from chathouse.utilities.security.token import Token
from chathouse.service import UserService
from flask import current_app
from chathouse.socket import socket
from tests.base import BaseTestCase
import time

class NotificationTestCase(BaseTestCase):

	'''
	NotificationTestCase - class aimed at testing different requests aimed at the Socket Namespace : /socket/notification.
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

		self.namespace='/socket/notification'

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
		Goal: test a valid connection call - which performs a "handshake", with necessary authorized credentials - access token.
		'''
		user = self.prepare_user()

		access_token = self.access_token(activity=user.activity_state,user_id=user.id)

		client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})

		self.assertTrue(client.is_connected(self.namespace))

		self.discharge_user()

	def test_invalid_connect_authorization_access_token_absent(self):
		'''
		Goal: test an invalid connection call. Invalid according to the absence of the authorization.
		'''
		user = self.prepare_user()

		client = self.socket.test_client(self.app,namespace=self.namespace)

		self.assertFalse(client.is_connected(self.namespace))

		self.discharge_user()

	def test_invalid_connect_authorization_invalid_token_type(self):
		'''
		Goal: test an invalid connection call. Invalid according to providing valid grant token as authorization , instead of an access token.
		'''
		user = self.prepare_user()

		access_token = self.access_token(activity=user.activity_state,user_id=user.id,token_type='grant')

		client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})

		self.assertFalse(client.is_connected(self.namespace))

		self.discharge_user()

	def test_invalid_connect_authorization_expired(self):
		'''
		Goal: test an invalid connection call. Invalid according to the lifetime of the authorization token - ie token has expired.
		'''
		user = self.prepare_user()

		access_token = self.access_token(activity=user.activity_state,user_id=user.id,exp={'seconds':1})

		time.sleep(2)

		client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})

		self.assertFalse(client.is_connected(self.namespace))

		self.discharge_user()

	def test_invalid_connect_authorization_access_token_invalid_activity(self):
		'''
		Goal: test an invalid connection call. Invalid according to the activity state of the user - ie the token has been revoked. Example the user has logged out.
		'''
		user = self.prepare_user()

		access_token = self.access_token(activity=user.activity_state,user_id=user.id)

		time.sleep(1)
		user.update_activity()

		client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})

		self.assertFalse(client.is_connected(self.namespace))

		self.discharge_user()
	
	def test_invalid_connect_authorization_access_token_invalid_datatypes(self):
		'''
		Goal: test an invalid connection call. Invalid according to the datatype of one of the crucial keys.
		'''
		user = self.prepare_user()

		access_token = self.access_token(activity='dummy',user_id=user.id)

		client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
	
		self.assertFalse(client.is_connected(self.namespace))

		self.discharge_user()

	#Establish a chat
	def test_valid_storage_chat_establishment(self):
		'''
		Goal: test a valid establish_a_chat call.
		Actions: connect to a notification socket, then estalish a "self chat" - storage.
		'''
		user = self.prepare_user()
		access_token = self.access_token(activity=user.activity_state,user_id=user.id)
		
		chat_name='A test storage chat'
		
		client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		
		self.assertTrue(client.is_connected(self.namespace))

		client.emit('establish_a_chat',{'name':chat_name},namespace=self.namespace)

		response=client.get_received(self.namespace)

		self.assertEqual('established_chat',response[0].get('name',''))

		self.assertIn('id',response[0].get('args',[{}])[0])

		self.assertIn('name',response[0].get('args',[{}])[0])

		self.assertEqual(chat_name,response[0]['args'][0]['name'])

		self.discharge_user()

	def test_valid_chat_establishment(self):
		'''
		Goal: test a valid establish_a_chat call.
		Actions:
			1.Prepare users and respective connections to the /notification.
			2.Verify the connections.
			3.Establish a chat.
			4.Store the reponses and validate separately.
			5.Make sure that the established chat identifications are the same.
		'''
		#Prepare users
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)

		#Estalish connections for both clients
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		current_client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id)
		other_client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		
		chat_name='A test conversation chat'
		
		#Verify the authorized connections
		self.assertTrue(current_client.is_connected(self.namespace))

		self.assertTrue(other_client.is_connected(self.namespace))

		#Estalish a chat
		current_client.emit('establish_a_chat',{'name':chat_name, 'participant_id':other_user.id},namespace=self.namespace)

		#Store the responses
		current_response=current_client.get_received(self.namespace)
		other_response=other_client.get_received(self.namespace)

		asserts = lambda response,name: (a for a in (\
			self.assertEqual('established_chat',response[0].get('name','')),\
			self.assertIn('id',response[0].get('args',[{}])[0]),\
			self.assertIn('name',response[0].get('args',[{}])[0]),\
			self.assertEqual(name,response[0]['args'][0]['name'])) )		

		#Validate each response
		asserts(current_response,chat_name)
		asserts(other_response,chat_name)

		#Make sure of the accord between the chat identifications
		get_chat_id = lambda response: response[0]['args'][0]['id']
		self.assertEqual(*(get_chat_id(case) for case in (current_response,other_response)))
		
		self.discharge_user()
		self.discharge_user(1)

	#Discharge a chat
	def test_valid_chat_discharge(self):
		'''
		Goal: test a valid discharge_a_chat call.
		Actions:
			1.Prepare users and estalish connections for such clients.
			2.Let any of the sides estalish a chat.
			3.Make sure that the chat identifications are the same
			4.Any participant discharges a chat
			5.Store the responses for both sides and validate each of them
		'''
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)
		chat_name='A test conversation chat'

		#Estalish connections for both clients
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		current_client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id)
		other_client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		
		#Prepare a chat
		chat_id=current_user.establish_a_chat(chat_name).id
		#Prepare both participations
		current_user.join_a_chat(chat_id)
		other_user.join_a_chat(chat_id)

		#Any participant discharges a chat
		other_client.emit('discharge_a_chat',{'id':chat_id},namespace=self.namespace)

		#Store the responses for both sides
		current_response=current_client.get_received(self.namespace)
		other_response=other_client.get_received(self.namespace)


		asserts = lambda response,identification: (a for a in (\
			self.assertEqual('discharged_chat',response[0].get('name','')),\
			self.assertIn('id',response[0].get('args',[{}])[0]),\
			self.assertEqual(identification,response[0]['args'][0]['id'])) )

		#Validate each response
		asserts(current_response,chat_id)
		asserts(other_response,chat_id)

		self.discharge_user()
		self.discharge_user(1)
	
	def test_invalid_chat_discharge_invalid_payload_keys(self):
		'''
		Goal: test an invalid discharge_a_chat call.
		Actions:
			1.Prepare users and estalish connections for such clients.
			2.Prepare a chat with respective participations.
			3.Any participant discharges a chat - invalid provided payload - identification key instead of id
			4.Validate the presence of the error response.
		'''
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)
		chat_name='A test conversation chat'

		#Estalish connections for both clients
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		current_client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id)
		other_client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		
		#Prepare a chat
		chat_id=current_user.establish_a_chat(chat_name).id
		#Prepare both participations
		current_user.join_a_chat(chat_id)
		other_user.join_a_chat(chat_id)

		#Any participant discharges a chat
		other_client.emit('discharge_a_chat',{'identification':chat_id},namespace=self.namespace)
		
		self.assertEqual('error',other_client.get_received(self.namespace)[0].get('name',''))

		self.discharge_user()
		self.discharge_user(1)

	def test_invalid_chat_discharge_unauthorized(self):
		'''
		Goal: test an invalid discharge_a_chat call.
		Actions:
			1.Prepare users and estalish connections for such clients.
			2.Prepare a chat with a single participation.
			3.Excluded user tries to discharge a chat.
			4.Validate the presence of the error response.
		'''
		current_user = self.prepare_user()
		other_user = self.prepare_user(1)
		chat_name='A test conversation chat'

		#Estalish connections for both clients
		access_token = self.access_token(activity=current_user.activity_state,user_id=current_user.id)
		current_client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		
		access_token = self.access_token(activity=other_user.activity_state,user_id=other_user.id)
		other_client = self.socket.test_client(self.app,namespace=self.namespace ,headers={'Authorization':f'Bearer {access_token.value}'})
		
		#Prepare a chat
		chat_id=current_user.establish_a_chat(chat_name).id
		#Prepare a single participation
		current_user.join_a_chat(chat_id)

		#Any participant discharges a chat
		other_client.emit('discharge_a_chat',{'id':chat_id},namespace=self.namespace)
		
		response=other_client.get_received(self.namespace)
		self.assertEqual('error',response[0].get('name',''))

		self.discharge_user()
		self.discharge_user(1)




