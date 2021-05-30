from chathouse import create_app
import unittest

class BaseTestCase(unittest.TestCase):
	'''
	A BaseTestCase - meant serve as core of the other tests.
	'''
	@classmethod
	def setUpClass(cls):
		cls.app=create_app('Testing')
		cls.app_context=cls.app.app_context()
		cls.app_context.push()
