from chathouse.utilities.security.token import Token
from chathouse.service import UserService
from flask import current_app
from tests.base import BaseTestCase
import time,copy

class VerificationTestCase(BaseTestCase):

	'''
	VerificationTestCase - class aimed at testing different requests aimed at the REST endpoint : /api/tokens/verification.
	'''


	def setUp(self):
		self.dummy_identification_payload={'signup':{
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

#Signup
	def test_valid_verification_signup(self):
		'''
		Goal: test verification request aimed at the signup with valid body & headers.
		'''
		client = self.app.test_client()

		valid_preaccess_token = Token(payload_data={'route':'signup','token_type':'preaccess','exp':current_app.config['PREACCESS_EXP']})
		client.set_cookie('','preaccess_token',valid_preaccess_token.value)
		response=client.post('/api/tokens/verification',json=self.dummy_identification_payload['signup'])
		self.assertEqual(response.status_code,201)


	#Invalid
	#BadRequest
	def test_bad_request_verification_signup_data_type(self):
		'''
		Goal test requests with invalid bodies - incorrect datatype.
		Actions: dummy_payload is invalid : incorrect datatype.
		'''
		client = self.app.test_client()

		valid_preaccess_token = Token(payload_data={'route':'signup','token_type':'preaccess','exp':current_app.config['PREACCESS_EXP']})
		client.set_cookie('','preaccess_token',valid_preaccess_token.value)
		invalid_payload=copy.deepcopy(self.dummy_identification_payload['signup'])
		invalid_payload['name']=['name']
		response=client.post('/api/tokens/verification',json=invalid_payload)
		self.assertEqual(response.status_code,400)

	def test_bad_request_verification_signup_absent_key(self):
		'''
		Goal test requests with invalid bodies - incorrect keys.
		Actions: dummy_payload is invalid : incorrect key/value pairs.
		'''
		client = self.app.test_client()

		valid_preaccess_token = Token(payload_data={'route':'signup','token_type':'preaccess','exp':current_app.config['PREACCESS_EXP']})
		client.set_cookie('','preaccess_token',valid_preaccess_token.value)
		invalid_payload=copy.deepcopy(self.dummy_identification_payload['signup'])
		invalid_payload.pop('name')
		response=client.post('/api/tokens/verification',json=invalid_payload)
		self.assertEqual(response.status_code,400)

	#Unauthorized
	def test_unauthorized_verification_signup_preaccess_token_type_invalid(self):
		'''
		Goal: test invalid authorization - the preaccess token /w invalid type.
		Actions: dymmy_payload is valid according to the signup , token type is invalid:
		'''
		client = self.app.test_client()

		invalid_preaccess_token=Token(payload_data={'route':'signup','token_type':'access','exp':current_app.config['PREACCESS_EXP']})
		client.set_cookie('','preaccess_token',invalid_preaccess_token.value)
		response=client.post('/api/tokens/verification',json=self.dummy_identification_payload['signup'])
		self.assertEqual(response.status_code,401)
	
	def test_unauthorized_verification_signup_preaccess_token_type_absent(self):
		'''
		Goal: test invalid authorization - the preaccess token /w absent type.
		Actions: dymmy_payload is valid according to the signup , token type is absent:
		'''
		client = self.app.test_client()

		invalid_preaccess_token=Token(payload_data={'route':'signup','exp':current_app.config['PREACCESS_EXP']})
		client.set_cookie('','preaccess_token',invalid_preaccess_token.value)
		response=client.post('/api/tokens/verification',json=self.dummy_identification_payload['signup'])
		self.assertEqual(response.status_code,401)
	
	def test_unauthorized_verification_signup_preaccess_route_invalid(self):
		'''
		Goal: test invalid authorization - the preaccess token /w invalid route.
		Actions: dymmy_payload is valid according to the signup , route is invalid:
		'''
		client = self.app.test_client()

		invalid_preaccess_token=Token(payload_data={'route':'invalid','token_type':'preaccess','exp':current_app.config['PREACCESS_EXP']})
		client.set_cookie('','preaccess_token',invalid_preaccess_token.value)
		response=client.post('/api/tokens/verification',json=self.dummy_identification_payload['signup'])
		self.assertEqual(response.status_code,401)

	def test_unauthorized_verification_signup_preaccess_route_absent(self):
		'''
		Goal: test invalid authorization - the preaccess token /w absent route.
		Actions: dymmy_payload is valid according to the signup , route is absent:
		'''
		client = self.app.test_client()

		invalid_preaccess_token=Token(payload_data={'token_type':'preaccess','exp':current_app.config['PREACCESS_EXP']})
		client.set_cookie('','preaccess_token',invalid_preaccess_token.value)
		response=client.post('/api/tokens/verification',json=self.dummy_identification_payload['signup'])
		self.assertEqual(response.status_code,401)

	def test_unauthorized_verification_signup_preaccess_signature_expired(self):
		'''
		Goal: test invalid authorization - the preaccess token /w expired signature.
		Actions: dymmy_payload is valid according to the signup , signature has expired:
		'''
		client = self.app.test_client()

		invalid_preaccess_token=Token(payload_data={'route':'signup','token_type':'preaccess','exp':{'seconds':0}})
		time.sleep(1)
		client.set_cookie('','preaccess_token',invalid_preaccess_token.value)
		response=client.post('/api/tokens/verification',json=self.dummy_identification_payload['signup'])
		self.assertEqual(response.status_code,401)

#Login
	#Valid
	def test_valid_verification_login(self):
		'''
		Goal: test verification request aimed at the login with valid body & headers.
		'''
		self.prepare_user()

		client = self.app.test_client()

		valid_preaccess_token = Token(payload_data={'route':'login','token_type':'preaccess','exp':current_app.config['PREACCESS_EXP']})
		client.set_cookie('','preaccess_token',valid_preaccess_token.value)
		response=client.post('/api/tokens/verification',json=self.dummy_identification_payload['login'])
		self.assertEqual(response.status_code,201)

		self.discharge_user()

	#Invalid
	#Bad request

	def test_bad_request_verification_login_data_type(self):
		'''
		Goal test requests with invalid bodies - incorrect datatype.
		Actions: dummy_payload is invalid : incorrect datatype.
		'''

		self.prepare_user()

		client = self.app.test_client()

		valid_preaccess_token = Token(payload_data={'route':'login','token_type':'preaccess','exp':current_app.config['PREACCESS_EXP']})
		client.set_cookie('','preaccess_token',valid_preaccess_token.value)
		invalid_payload=copy.deepcopy(self.dummy_identification_payload['login'])
		invalid_payload['identification']=1
		response=client.post('/api/tokens/verification',json=invalid_payload)
		self.assertEqual(response.status_code,400)

		self.discharge_user()

	def test_bad_request_verification_login_absent(self):
		'''
		Goal test requests with invalid bodies - incorrect user identification - absent user.
		Actions: dummy_payload is invalid : absent user.
		'''
		client = self.app.test_client()

		valid_preaccess_token = Token(payload_data={'route':'login','token_type':'preaccess','exp':current_app.config['PREACCESS_EXP']})
		client.set_cookie('','preaccess_token',valid_preaccess_token.value)
		invalid_payload=copy.deepcopy(self.dummy_identification_payload['login'])
		response=client.post('/api/tokens/verification',json=invalid_payload)
		
		self.assertEqual(response.status_code,400)

	#Unauthorized
	def test_unauthorized_verification_login_preaccess_token_type_invalid(self):
		'''
		Goal: test invalid authorization - the preaccess token /w invalid type.
		Actions: dymmy_payload is valid according to the login , token type is invalid:
		'''
		
		self.prepare_user()

		client = self.app.test_client()

		invalid_preaccess_token=Token(payload_data={'route':'login','token_type':'access','exp':current_app.config['PREACCESS_EXP']})
		client.set_cookie('','preaccess_token',invalid_preaccess_token.value)
		response=client.post('/api/tokens/verification',json=self.dummy_identification_payload['login'])
		self.assertEqual(response.status_code,401)

		self.discharge_user()
	
	def test_unauthorized_verification_login_preaccess_token_type_absent(self):
		'''
		Goal: test invalid authorization - the preaccess token /w absent type.
		Actions: dymmy_payload is valid according to the login , token type is absent:
		'''
		self.prepare_user()

		client = self.app.test_client()

		invalid_preaccess_token=Token(payload_data={'route':'login','exp':current_app.config['PREACCESS_EXP']})
		client.set_cookie('','preaccess_token',invalid_preaccess_token.value)
		response=client.post('/api/tokens/verification',json=self.dummy_identification_payload['login'])
		self.assertEqual(response.status_code,401)
		
		self.discharge_user()
	
	def test_unauthorized_verification_login_preaccess_route_invalid(self):
		'''
		Goal: test invalid authorization - the preaccess token /w invalid route.
		Actions: dymmy_payload is valid according to the login , route is invalid:
		'''
		self.prepare_user()

		client = self.app.test_client()

		invalid_preaccess_token=Token(payload_data={'route':'invalid','token_type':'preaccess','exp':current_app.config['PREACCESS_EXP']})
		client.set_cookie('','preaccess_token',invalid_preaccess_token.value)
		response=client.post('/api/tokens/verification',json=self.dummy_identification_payload['login'])
		self.assertEqual(response.status_code,401)

		self.discharge_user()


	def test_unauthorized_verification_login_preaccess_route_absent(self):
		'''
		Goal: test invalid authorization - the preaccess token /w absent route.
		Actions: dymmy_payload is valid according to the login , route is absent:
		'''
		self.prepare_user()

		client = self.app.test_client()

		invalid_preaccess_token=Token(payload_data={'token_type':'preaccess','exp':current_app.config['PREACCESS_EXP']})
		client.set_cookie('','preaccess_token',invalid_preaccess_token.value)
		response=client.post('/api/tokens/verification',json=self.dummy_identification_payload['login'])
		self.assertEqual(response.status_code,401)

		self.discharge_user()

	def test_unauthorized_verification_login_preaccess_signature_expired(self):
		'''
		Goal: test invalid authorization - the preaccess token /w expired signature.
		Actions: dymmy_payload is valid according to the login , signature has expired:
		'''
		self.prepare_user()

		client = self.app.test_client()

		invalid_preaccess_token=Token(payload_data={'route':'login','token_type':'preaccess','exp':{'seconds':0}})
		time.sleep(1)
		client.set_cookie('','preaccess_token',invalid_preaccess_token.value)
		response=client.post('/api/tokens/verification',json=self.dummy_identification_payload['login'])
		self.assertEqual(response.status_code,401)

		self.discharge_user()