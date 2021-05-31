from chathouse.utilities.security.token import Token
from chathouse.service import UserService
from flask import current_app
from tests.base import BaseTestCase
import time

class AccessTestCase(BaseTestCase):

	'''
	AccessTestCase - class aimed at testing different requests aimed at the REST endpoint : /api/tokens/access.
	'''

	def setUp(self):
		
		self.grant_token = lambda **update: Token(payload_data={'token_type':'grant','exp':current_app.config['GRANT_EXP'],**update})
		
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
		return user
		#assert user.signup(**payload), ValueError('Couldn\'t prepare a test user.')

	def discharge_user(self):
		user=UserService(username='test_username')
		user.remove()
		#assert user.remove(), ValueError('Coudn\'t find a test user to remove.')

#Signup
	#Valid
	def test_valid(self):
		'''
		Goal: test a valid request to get the access token, providing correct grant_token.
		'''
		user = self.prepare_user()

		grant_token = self.grant_token(activity=user.activity_state,user_id=user.id)

		client = self.app.test_client()

		response = client.get('/api/tokens/access',headers={'Authorization':f'Bearer {grant_token.value}'})

		self.assertEqual(response.status_code,200)

		self.assertIn('access_token',response.json)

		self.discharge_user()

	#Invalid
	def test_invalid_activity(self):
		'''
		Goal: test an invalid request to get the access token. Invalid according the updated activity.
		Example: user has logged out.
		'''
		user = self.prepare_user()

		grant_token = self.grant_token(activity=user.activity_state,user_id=user.id)

		user.update_activity()

		time.sleep(5)

		client = self.app.test_client()

		response = client.get('/api/tokens/access',headers={'Authorization':f'Bearer {grant_token.value}'})

		self.assertEqual(response.status_code,401)

		self.discharge_user()