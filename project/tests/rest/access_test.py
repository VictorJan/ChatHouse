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
		'''
		Goal: set up necessary instance attributes - during every test:
			grant_token:lambda function - generates a Token instance , meant to be used as a grant token.
				Parameters:update - key word argument - meant to store data required for the grant tokens , according to established guidelines - activity and user_id.
				Returns: Token instance
			dummy_identification_paylaod:dict - a dictionary which shall contain identification payloads for the actions , such as : signup or login.
		Returns: None
		'''
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
	def test_invalid_absent_grant_token(self):
		'''
		Goal: test an invalid request to get the access token. Invalid according to the absence of the authorization grant token.
		'''
		client = self.app.test_client()

		response = client.get('/api/tokens/access')

		self.assertEqual(response.status_code,401)

	def test_invalid_expired_grant_token(self):
		'''
		Goal: test an invalid request to get the access token. Invalid according to the incorrect authorization token.
		'''
		user = self.prepare_user()

		grant_token = self.grant_token(activity=user.activity_state,user_id=user.id,exp={'seconds':1})

		client = self.app.test_client()

		time.sleep(2)

		response = client.get('/api/tokens/access',headers={'Authorization':f'Bearer {grant_token.value}'})

		self.assertEqual(response.status_code,401)

		self.discharge_user()


	def test_invalid_grant_token_activity(self):
		'''
		Goal: test an invalid request to get the access token. Invalid according to the updated activity.
		Example: user has logged out.
		'''
		user = self.prepare_user()

		grant_token = self.grant_token(activity=user.activity_state,user_id=user.id)

		time.sleep(2)
		
		user.update_activity()

		client = self.app.test_client()

		response = client.get('/api/tokens/access',headers={'Authorization':f'Bearer {grant_token.value}'})

		self.assertEqual(response.status_code,401)

		self.discharge_user()

	def test_invalid_grant_token_datatypes(self):
		'''
		Goal: test an invalid request to get the access token. Invalid according to the datatype of one of the crucial keys.
		'''
		user = self.prepare_user()

		grant_token = self.grant_token(activity='dummy',user_id=user.id)

		client = self.app.test_client()

		response = client.get('/api/tokens/access',headers={'Authorization':f'Bearer {grant_token.value}'})

		self.assertEqual(response.status_code,401)

		self.discharge_user()

	def test_invalid_grant_token_keys(self):
		'''
		Goal: test an invalid request to get the access token. Invalid according to the absence of some obligatory keys.
		'''
		user = self.prepare_user()

		grant_token = self.grant_token(user_id=user.id)

		client = self.app.test_client()

		response = client.get('/api/tokens/access',headers={'Authorization':f'Bearer {grant_token.value}'})

		self.assertEqual(response.status_code,401)

		self.discharge_user()