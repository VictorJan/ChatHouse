from chathouse.utilities.security.token import Token
from chathouse.service import UserService
from flask import current_app
from tests.base import BaseTestCase
import time

class GrantTestCase(BaseTestCase):

	'''
	GrantTestCase - class aimed at testing different requests aimed at the REST endpoint : /api/tokens/grant.
	'''

	def setUp(self):
		
		self.preaccess_token = lambda route: Token(payload_data={'route':route,'token_type':'preaccess','exp':current_app.config['PREACCESS_EXP']})
		
		self.verification_token = lambda **update: Token(payload_data={'token_type':'verification','exp':current_app.config['VERIFICATION_EXP'],**update})
		
		self.dummy_auth_payload={'signup':{
				'password':'9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
				'keyring':{
					'public_key':5,
					'g':9055,
					'm':9059,
					'private_key':{
						'iv':'str',
						'data':'str'
					}
				}
			},
			'login':{
				'password':'9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
			}
		}

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

	def prepare_user(self):
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
		user.signup(**payload)
		#assert user.signup(**payload), ValueError('Couldn\'t prepare a test user.')

	def discharge_user(self):
		user=UserService(username='test_username')
		user.remove()
		#assert user.remove(), ValueError('Coudn\'t find a test user to remove.')

#Signup
	#Valid
	def test_valid_signup(self):
		'''
		Goal: test a request aimed at the signup, providing valid json,header /w absent user.
		'''

		preaccess_token=self.preaccess_token('signup')

		verification_token=self.verification_token(identification_data=self.dummy_identification_payload['signup'],preaccess=preaccess_token.value,activity=0)

		client = self.app.test_client()

		response = client.post('/api/tokens/grant',headers={'Authorization':f'Bearer {verification_token.value}'},json=self.dummy_auth_payload['signup'])

		self.assertEqual(response.status_code,201)

		self.assertIn('grant_token',response.json)

		self.discharge_user()

	#Invalid
	def test_invalid_signup_exists(self):
		'''
		Goal: test a request aimed at the signup, providing identification data for already existing user.
		'''
		self.prepare_user()

		preaccess_token=self.preaccess_token('signup')

		verification_token=self.verification_token(identification_data=self.dummy_identification_payload['signup'],preaccess=preaccess_token.value,activity=0)

		client = self.app.test_client()

		response = client.post('/api/tokens/grant',headers={'Authorization':f'Bearer {verification_token.value}'},json=self.dummy_auth_payload['signup'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()
	
	def test_invalid_signup_paylod(self):
		'''
		Goal: test a request aimed at the signup, providing identification data for already existing user.
		'''
		self.prepare_user()

		preaccess_token=self.preaccess_token('signup')

		verification_token=self.verification_token(identification_data=self.dummy_identification_payload['signup'],preaccess=preaccess_token.value,activity=0)

		client = self.app.test_client()

		response = client.post('/api/tokens/grant',headers={'Authorization':f'Bearer {verification_token.value}'},json=self.dummy_auth_payload['signup'])

		self.assertEqual(response.status_code,401)

		self.discharge_user()

#Login
	#Valid
	def test_valid_login(self):
		'''
		Goal: test a request aimed at the signup, providing valid json,header /w absent user.
		'''
		self.prepare_user()

		preaccess_token=self.preaccess_token('login')

		verification_token=self.verification_token(identification_data=self.dummy_identification_payload['login'],preaccess=preaccess_token.value,activity=(UserService(username='test_username')).activity_state)

		client = self.app.test_client()

		response = client.post('/api/tokens/grant',headers={'Authorization':f'Bearer {verification_token.value}'},json=self.dummy_auth_payload['login'])

		self.assertEqual(response.status_code,201)

		self.assertIn('grant_token',response.json)

		self.discharge_user()

	#Invalid
	def test_invalid_login_absent(self):
		'''
		Goal: test a request aimed at the login, providing data for a user that doesn't exist , has been discharged after the generation of a verification token.
		Verifies, that the verification token would be denied according to the activity state update or better say absense of such.
		'''

		preaccess_token=self.preaccess_token('login')
		self.discharge_user()
		self.prepare_user()

		verification_token=self.verification_token(identification_data=self.dummy_identification_payload['login'],preaccess=preaccess_token.value,activity=(UserService(username='test_username')).activity_state)

		self.discharge_user()

		client = self.app.test_client()

		response = client.post('/api/tokens/grant',headers={'Authorization':f'Bearer {verification_token.value}'},json=self.dummy_auth_payload['login'])

		self.assertEqual(response.status_code,401)

	def test_invalid_login_invalid_activity(self):
		'''
		Goal: test a request aimed at the signup, providing identification data for already existing user.
		Verifies, that the verification token would be denied according to the activity state update.
		'''

		preaccess_token=self.preaccess_token('login')
		
		self.prepare_user()

		user=UserService(username='test_username')

		verification_token=self.verification_token(identification_data=self.dummy_identification_payload['login'],preaccess=preaccess_token.value,activity=user.activity_state)

		time.sleep(5)

		user.update_activity()

		
		client = self.app.test_client()

		response = client.post('/api/tokens/grant',headers={'Authorization':f'Bearer {verification_token.value}'},json=self.dummy_auth_payload['login'])

		self.assertEqual(response.status_code,401)