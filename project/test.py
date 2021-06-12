if __name__=='__main__':
	import unittest
	tests = unittest.TestLoader().discover('',pattern='*_test.py')
	unittest.TextTestRunner(verbosity=2).run(tests)