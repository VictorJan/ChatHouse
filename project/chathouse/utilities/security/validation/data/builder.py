from abc import ABC,abstractmethod
class Builder(ABC):

	'''
	Builder - an abstract class meant to be implemented with contructive and productive functionalities aimed at the Template/Field instances.
	Inherits: ABC.
	
	Methods:
		add(self,component):
			Goal:shall provide an application of a certain contruction capabilities.
	Properties:
		product - shall provide a result of the contruction, containing productive features. 
	'''
	
	@abstractmethod
	def add(self,component):
		pass
	
	@property
	@abstractmethod
	def product(self):
		pass