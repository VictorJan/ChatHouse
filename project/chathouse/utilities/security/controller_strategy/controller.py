from chathouse.utilities.security.controller_strategy.strategy import Strategy

class Controller:
	def __init__(self,strategy):
		assert issubclass(strategy.__class__,Strategy),TypeError('Class of a strategy argument must be a subclass of the Strategy class.')
		self.__strategy=strategy

	def handle(self,headers,data,**kwargs):
		return self.__strategy.accept(headers,data,**kwargs)

	@property
	def strategy(self):
		return self.__strategy