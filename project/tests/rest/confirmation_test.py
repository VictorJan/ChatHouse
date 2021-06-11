from chathouse.utilities.security.token import Token
from chathouse.service import UserService
from flask import current_app
from tests.base import BaseTestCase
import time

class ConfirmationTestCase(BaseTestCase):

	'''
	ConfirmationTestCase - class aimed at testing different requests aimed at the REST endpoint : /api/tokens/confirmation.
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
		
		self.dummy_identification_payload={
			'signup':{
				'email':'chathousetestclient@gmail.com',
				'username':'test_username',
				'name':'Testname',
				'about':'test_about'
			},
			'login':{
				'identification':'test_username'
			}
		}

		self.dummy_json_payload={
			'put':{'action':'put'},
			'delete':{'action':'delete'}
		}


	def prepare_user(self):
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
				**self.dummy_identification_payload['signup']
			},
			'key_data':{
				'public_key':5,
				'private_key':{'iv':'str','data':'str'}
			}
		}

		try:
			assert user.signup(**payload), ValueError('Couldn\'t prepare a test user.')
		except:
			self.discharge_user()
			assert user.signup(**payload), ValueError('Still couldn\'t prepare a test user.')

		return user

	def discharge_user(self):
		'''
		Goal: remove/delete a test user instance.
		Returns:None
		Exceptions:
			Raises:
				ValueError - in cases,when one tries to discharge a user instance, which is not related to any user. 
		'''
		user=UserService(username='test_username')
		assert user.remove(), ValueError('Coudn\'t find a test user to remove.')

	#Valid
	def test_valid_put(self):
		'''
		Goal: test a valid request to create a confirmation token for the password reset - put action, providing correct access_token.
		'''
		user = self.prepare_user()

		access_token = self.access_token(activity=user.activity_state,user_id=user.id)

		client = self.app.test_client()

		response = client.post('/api/tokens/confirmation',headers={'Authorization':f'Bearer {access_token.value}'},json=self.dummy_json_payload['put'])

		self.assertEqual(response.status_code,201)

		self.discharge_user()

	def test_valid_delete(self):
		'''
		Goal: test a valid request to create a confirmation token for the account discharge - delete action, providing correct access_token.
		'''
		user = self.prepare_user()

		access_token = self.access_token(activity=user.activity_state,user_id=user.id)

		client = self.app.test_client()

		response = client.post('/api/tokens/confirmation',headers={'Authorization':f'Bearer {access_token.value}'},json=self.dummy_json_payload['delete'])

		self.assertEqual(response.status_code,201)

		self.discharge_user()

	#Invalid
	def test_invalid_payload_invalid_action(self):
		'''
		Goal: test an invalid request to create a confirmation token, providing invalid action in the payload.
		'''
		user = self.prepare_user()

		access_token = self.access_token(activity=user.activity_state,user_id=user.id)

		client = self.app.test_client()

		response = client.post('/api/tokens/confirmation',headers={'Authorization':f'Bearer {access_token.value}'},json={'action':'post'})

		self.assertEqual(response.status_code,400)

		self.discharge_user()

	def test_invalid_payload_invalid_nesting(self):
		'''
		Goal: test an invalid request to create a confirmation token, providing invalid action in the payload.
		'''
		user = self.prepare_user()

		access_token = self.access_token(activity=user.activity_state,user_id=user.id)

		client = self.app.test_client()

		response = client.post('/api/tokens/confirmation',headers={'Authorization':f'Bearer {access_token.value}'},json=self.dummy_json_payload)

		self.assertEqual(response.status_code,400)

		self.discharge_user()

	def test_invalid_authorization_absent_access_token(self):
		'''
		Goal: test an invalid request to create a confirmation token. Invalid according to the absence of the authorization - access token.
		'''
		user = self.prepare_user()

		client = self.app.test_client()

		response = client.post('/api/tokens/confirmation',json=self.dummy_json_payload['delete'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()

	def test_invalid_authorization_expired_access_token(self):
		'''
		Goal: test an invalid request to create a confirmation token. Invalid according to the expired access token.
		'''
		user = self.prepare_user()

		access_token = self.access_token(activity=user.activity_state,user_id=user.id, exp={'seconds':1})

		client = self.app.test_client()

		time.sleep(2)

		response = client.post('/api/tokens/confirmation',headers={'Authorization':f'Bearer {access_token.value}'},json=self.dummy_json_payload['delete'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()

	def test_invalid_authorization_expired_access_token(self):
		'''
		Goal: test an invalid request to create a confirmation token. Invalid according to a activity state property of a user.Examples - token has been already used, user has logged out, ... .
		'''
		user = self.prepare_user()

		access_token = self.access_token(activity=user.activity_state,user_id=user.id)

		client = self.app.test_client()

		time.sleep(1)
		user.update_activity()

		response = client.post('/api/tokens/confirmation',headers={'Authorization':f'Bearer {access_token.value}'},json=self.dummy_json_payload['delete'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()

	def test_invalid_authorization_invalid_token_type(self):
		'''
		Goal: test an invalid request to create a confirmation token. Invalid according to valid grant token , instead of an access token.
		'''
		user = self.prepare_user()

		access_token = self.access_token(activity=user.activity_state,user_id=user.id,token_type='grant')

		client = self.app.test_client()

		response = client.post('/api/tokens/confirmation',headers={'Authorization':f'Bearer {access_token.value}'},json=self.dummy_json_payload['delete'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()

	def test_invalid_authorization_access_token_datatypes(self):
		'''
		Goal: test an invalid request to get the confirmation token. Invalid according to the datatype of one of the crucial keys.
		'''
		user = self.prepare_user()

		access_token = self.access_token(activity='dummy',user_id=user.id)

		client = self.app.test_client()

		response = client.post('/api/tokens/confirmation',headers={'Authorization':f'Bearer {access_token.value}'},json=self.dummy_json_payload['delete'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()

	def test_invalid_authorization_access_token_keys(self):
		'''
		Goal: test an invalid request to get the confirmation token. Invalid according to the absence of some obligatory keys.
		'''
		user = self.prepare_user()

		access_token = self.access_token(user_id=user.id)

		client = self.app.test_client()

		response = client.post('/api/tokens/confirmation',headers={'Authorization':f'Bearer {access_token.value}'},json=self.dummy_json_payload['delete'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()