from chathouse.utilities.security.validation.data.template import Template
from chathouse.utilities.security.validation.data.field import Field

from abc import ABC,abstractmethod
class Builder(ABC):
	
	@abstractmethod
	def add(self,Field):
		pass
	
	@property
	@abstractmethod
	def template(self):
		pass


class TemplateBuilder(Builder):
	def __init__(self):
		self.__reset()

	def add(self,field):
		assert isinstance(field,Field),ValueError('The field argument shall be an instance of the Field class')
		self.__template.add(field)
		return None

	def __reset(self):
		self.__template=Template()
		return None

	@property
	def template(self):
		running_template=self.__template
		self.__reset()
		return running_template
	
	