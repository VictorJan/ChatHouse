if __name__=='__main__':
	import unittest
	tests = unittest.TestLoader().discover('tests/socket',pattern='chat_test.py')
	unittest.TextTestRunner(verbosity=2).run(tests)