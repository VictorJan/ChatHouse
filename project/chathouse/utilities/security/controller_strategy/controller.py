from chathouse.utilities.security.controller_strategy.strategy import Strategy

class Controller:
	def __init__(self,strategy):
		assert isinstance(strategy,Strategy),TypeError('Instance of the strategy argument shall be derived from the Strategy class.')
		self.__strategy=strategy

	def handle(self,headers,data,**kwargs):
		return self.__strategy.accept(headers,data,**kwargs)

	@property
	def strategy(self):
		return self.__strategy