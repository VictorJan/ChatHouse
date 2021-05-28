from flask import current_app
from functools import wraps
from threading import Thread

def asynchronous(plea):
	'''
	Goal: prepare and start a provided request/plea as an asynchronous one - by executing a separate Thread.
	Arguments: plea - the function/method that has to run asynchronously.
	Actions:
		prepare:
			0.Get the app object using the current_app instance. Set an appropriate key for the current app object  - 'app'.
			1.Then start a new thread providing the inital plea/request/funtion/method and respective arguments,key word arguments.
	Raises:
		KeyError - If the key word argument contains an app key.
	Returns: prepare -> None.
	'''
	
	@wraps(plea)
	def prepare(*args,**kwargs):
		
		assert kwargs.get('app',None) is None, KeyError('The app shall be set up in the preparation stage, not provided as a key-word-argument.')
		
		kwargs['app']=current_app._get_current_object()
		
		Thread(target=plea, args=args, kwargs=kwargs).start()

		return None
		
	return prepare