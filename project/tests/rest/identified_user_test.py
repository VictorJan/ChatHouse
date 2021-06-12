from chathouse.utilities.security.token import Token
from chathouse.service import UserService
from flask import current_app
from tests.base import BaseTestCase
import time

class IdentifiedUserTestCase(BaseTestCase):

	'''
	IdentifiedUserTestCase - class aimed at testing different requests aimed at the REST endpoint : /api/users/<id>.
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
		self.confirmation_token = lambda **update: Token(payload_data={'token_type':'confirmation','exp':current_app.config['CONFIRMATION_EXP'],**update})
		
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

		self.dummy_action_payload={
			'put':{'action':'put'},
			'delete':{'action':'delete'}
		}

		self.dummy_json_payload={
			'put':{
				'reset':{
					'password':{
						'current':'9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
						'new':'9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a09'
					},
					'private_key':{
						'iv':'iv value',
						'data':'encrypted data'
					}
				}
			},
			'delete':{
				'password':'9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
			}
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
		Goal: test a valid request to execute a password reset - put action, providing correct authorization credentials: a confirmation_token and a payload of passwords:current,new and a private key.
		'''
		user = self.prepare_user()

		confirmation_token = self.confirmation_token(activity=user.activity_state,user_id=user.id,**self.dummy_action_payload['put'])

		client = self.app.test_client()

		response = client.put(f'/api/users/{user.id}',headers={'Authorization':f'Bearer {confirmation_token.value}'},json=self.dummy_json_payload['put'])

		self.assertEqual(response.status_code,200)

		self.discharge_user()

	def test_valid_delete(self):
		'''
		Goal: test a valid request to execute a account discharge - delete action, providing correct authorization,authentification credentials: a confirmation_token and a password.
		'''
		user = self.prepare_user()

		confirmation_token = self.confirmation_token(activity=user.activity_state,user_id=user.id,**self.dummy_action_payload['delete'])

		client = self.app.test_client()

		response = client.delete(f'/api/users/{user.id}',headers={'Authorization':f'Bearer {confirmation_token.value}'},json=self.dummy_json_payload['delete'])

		self.assertEqual(response.status_code,200)

	#Invalid
	def test_invalid_put_authorization_absent_confirmation_token(self):
		'''
		Goal: test an invalid request to execute a password reset - absence of an authorization credential.
		'''
		user = self.prepare_user()

		client = self.app.test_client()

		response = client.put(f'/api/users/{user.id}',json=self.dummy_json_payload['put'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()

	def test_invalid_put_authorization_expired_confirmation_token(self):
		'''
		Goal: test an invalid request to execute a password reset - the authorization credential - confirmation token has expired.
		'''
		user = self.prepare_user()

		confirmation_token = self.confirmation_token(activity=user.activity_state,user_id=user.id,**self.dummy_action_payload['put'],exp={'seconds':1})

		client = self.app.test_client()

		time.sleep(2)

		response = client.put(f'/api/users/{user.id}',headers={'Authorization':f'Bearer {confirmation_token.value}'},json=self.dummy_json_payload['put'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()
	
	def test_invalid_put_authorization_confirmation_token_activity(self):
		'''
		Goal: test an invalid request to execute a password reset - the authorization credential - the activity state is invalid - ie user has logged out.
		'''
		user = self.prepare_user()

		confirmation_token = self.confirmation_token(activity=user.activity_state,user_id=user.id,**self.dummy_action_payload['put'])

		client = self.app.test_client()

		time.sleep(1)
		user.update_activity()

		response = client.put(f'/api/users/{user.id}',headers={'Authorization':f'Bearer {confirmation_token.value}'},json=self.dummy_json_payload['put'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()

	def test_invalid_put_authentication(self):
		'''
		Goal: test an invalid request to execute a password reset - the authentication credentials - current password is not appropriate.
		'''
		user = self.prepare_user()

		confirmation_token = self.confirmation_token(activity=user.activity_state,user_id=user.id,**self.dummy_action_payload['put'])

		client = self.app.test_client()

		payload=self.dummy_json_payload['put']
		payload['reset']['password']['current']='5f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a03'

		response = client.put(f'/api/users/{user.id}',headers={'Authorization':f'Bearer {confirmation_token.value}'},json=self.dummy_json_payload['put'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()

	def test_invalid_delete_authorization_absent_confirmation_token(self):
		'''
		Goal: test an invalid request to execute an account discharge - absence of an authorization credential.
		'''
		user = self.prepare_user()

		client = self.app.test_client()

		response = client.delete(f'/api/users/{user.id}',json=self.dummy_json_payload['delete'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()

	def test_invalid_delete_authorization_expired_confirmation_token(self):
		'''
		Goal: test an invalid request to execute an account discharge - the authorization credential - confirmation token has expired.
		'''
		user = self.prepare_user()

		confirmation_token = self.confirmation_token(activity=user.activity_state,user_id=user.id,**self.dummy_action_payload['delete'],exp={'seconds':1})

		client = self.app.test_client()

		time.sleep(2)

		response = client.delete(f'/api/users/{user.id}',headers={'Authorization':f'Bearer {confirmation_token.value}'},json=self.dummy_json_payload['delete'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()
	
	def test_invalid_delete_authorization_confirmation_token_activity(self):
		'''
		Goal: test an invalid request to execute an account discharge - the authorization credential - the activity state is invalid - ie user has logged out.
		'''
		user = self.prepare_user()

		confirmation_token = self.confirmation_token(activity=user.activity_state,user_id=user.id,**self.dummy_action_payload['delete'])

		client = self.app.test_client()

		time.sleep(1)
		user.update_activity()

		response = client.delete(f'/api/users/{user.id}',headers={'Authorization':f'Bearer {confirmation_token.value}'},json=self.dummy_json_payload['delete'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()

	def test_invalid_delete_authentication(self):
		'''
		Goal: test an invalid request to execute an account discharge - the authentication credentials - provided password is not appropriate.
		'''
		user = self.prepare_user()

		confirmation_token = self.confirmation_token(activity=user.activity_state,user_id=user.id,**self.dummy_action_payload['delete'])

		client = self.app.test_client()

		payload=self.dummy_json_payload['delete']
		payload['password']='5f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a03'

		response = client.delete(f'/api/users/{user.id}',headers={'Authorization':f'Bearer {confirmation_token.value}'},json=self.dummy_json_payload['delete'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()