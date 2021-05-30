from chathouse.utilities.security.controller_strategy.strategy import Strategy

class Controller:
	'''
	Controller class - the initial governance point of managing any incoming requests. 
	Sets up / steers the flow in a certain direction -> to a specific Strategy, thus handling the forthcoming requests.

	Pattern/Chain of calls:
		Controller.handle(request_headers,request_data) -> ... -> any decorators|proxies -> ... -> ( Strategy.accept(request_headers,request_data,kwargs) ).
	
	Attributes:
		__strategy - an instance of a Strategy class.

	Methods:
		handle - directs the request headers and data to be accepted by the defined Strategy.
	Properties:
		strategy - returns the strategy attribute.
'''
	def __init__(self,strategy):
		'''
		Goal: initializes a Controller instance with a certain Strategy.
		Arguments: strategy:Strategy.
		Returns:None.
		Exceptions:
			Raises:
				TypeError - if the provided strategy is not an instance of the Strategy class.
		'''
		assert isinstance(strategy,Strategy),TypeError('Instance of the strategy argument shall be derived from the Strategy class.')
		self.__strategy=strategy

	def handle(self,headers,data,**kwargs):
		'''
		Goal: direct the initial flow towards the integrated Strategy instance, providing the incoming request headers, data and any key word arguments.
		Arguments: headers:dict(headers of a request), data:dict(a request's body), key-word-argument:dict(is meant to be used by any proxies or decorators , to store any resolved information)
		Returns: strategy's deecre/decision:(REST API:(status code, JSON) | View:(render of a template|redirect|make_response) | Socket Event:(None - inner emit|connect|disconnect is called) )
		'''
		return self.__strategy.accept(headers,data,**kwargs)

	@property
	def strategy(self):
		'''
		Goal: retreive the initialized strategy.
		Returns: defined strategy.
		'''
		return self.__strategy