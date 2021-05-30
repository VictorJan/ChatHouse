from chathouse.utilities.security.token import Token
from flask import current_app

from tests.base import BaseTestCase

class AuthenticationTestCase(BaseTestCase):

	def test_valid_signup_identification(self):
		'''
		Goal: test valid identification during the signup phase.
		Actions:Client must get the preaccess token - according to the route - signup
		'''
		client = self.app.test_client()
			
		client.get('/signup')
		
		payload={
			'email':'chathousetestclient@gmail.com',
			'username':'test_username',
			'name':'Testname',
			'about':'test_about'
		}
		
		response=client.post('/api/tokens/verification',json=payload)
		
		self.assertEqual(response.status_code,201)
		
	def test_invalid_signup_identification_preaccess(self):
		'''
		Goal: test valid identification during the signup phase.
		Actions:Client must get the preaccess token - according to the route - signup
		'''
		client = self.app.test_client()
		
		payload={
			'email':'chathousetestclient@gmail.com',
			'username':'test_username',
			'name':'Testname',
			'about':'test_about'
		}
		
		response=client.post('/api/tokens/verification',json=payload)

		self.assertEqual(response.status_code,401)
		self.assertEqual(response.json.get('message',None),"Unauthorized!")
		self.assertEqual(response.json.get('reason',None),"Invalid preaccess token.")

	def test_invalid_signup_identification_initial_route(self):
		'''
		Goal: test invalid identification during the signup phase.
		Actions:Client must gets the preaccess token - from the login route - and provides invalid payload.
		'''
		client = self.app.test_client()
		
		response=client.get('/login')
		
		payload={
			'email':'chathousetestclient@gmail.com',
			'username':'test_username',
			'name':'Testname',
			'about':'test_about'
		}
		
		'''
		verification_token=Token(payload_data={
			'identification_data':{'identification':'username'},
			'token_type':'verification',
			'activity':0,
			'preaccess':'response.head',
			'exp':current_app.config['VERIFICATION_EXP']
			})
		'''

		print(verification_token.value)

		response=client.post('/api/tokens/verification',json=payload)

		self.assertEqual(response.status_code,400)
		self.assertEqual(response.json.get('message',None),"Data is invalid.")
