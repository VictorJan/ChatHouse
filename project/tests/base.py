from chathouse import create_app
import unittest

class BaseTestCase(unittest.TestCase):
	'''
	A BaseTestCase - meant serve as core of the other tests.
	'''
	@classmethod
	def setUpClass(cls):
		'''
		Goal:sets up class attributes - app,app_context for further tests.
		Returns:None.
		'''
		cls.app=create_app('Testing')
		cls.app_context=cls.app.app_context()
		cls.app_context.push()
