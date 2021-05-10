from chathouse.utilities.security.controller_handler.handler import Handler

class Controller:
	def __init__(self,handler):
		if issubclass(handler.__class__,Handler):
			self.__handler=handler
		else:
			raise TypeError

	def handle(self,headers,data,**kwargs):
		return self.__handler.accept(headers,data,**kwargs)

	@property
	def handler(self):
		return self.__handler