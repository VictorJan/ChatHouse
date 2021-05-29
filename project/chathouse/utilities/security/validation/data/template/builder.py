from chathouse.utilities.security.validation.data.builder import Builder
from chathouse.utilities.security.validation.data.template import Template
from chathouse.utilities.security.validation.data.field import Field

class TemplateBuilder(Builder):
	'''
	TemplateBuilder - a class meant to implement contructive and productive functionalities aimed at the Template instances.
	Inherits: ABC.
	Flow:
		1.Initialize a TemplateBuilder -> which calls the __reset;
		[1.2.The call to __reset - sets up inital __field to an empty Template.]
		2.Perform construction - add components - Field_s.
		3.To end the construction stage, use the product property, which retreives the built Template instance and resets the Builder to the initial step, using the __reset call.
	
	Methods:
		__reset(self) - sets the Builder to the initial state.
		add(self,component) - executes contruction capabilities, providing the Field instances as components of the Template.

	Properties:
		product - provide a result of the contruction, containing productive features, and set the builder to the initial state.
	'''
	
	def __init__(self):
		'''
		Goal: initialize the Builder, by setting it to the initial state - using the reset call.
		Returns:None 
		'''
		self.__reset()

	def __reset(self):
		'''
		Goal: sets the Builder to initial state - fully initialized.
		Action: set the __template to an empty Template.
		Returns:None.
		'''
		self.__template=Template()
		return None

	def add(self,component):
		'''
		Goal: execute a part of the construction/building process - component injection.
		Arguments: component:Field.
		Actions:
			Adds a Field to the initialized Template.
		Returns None.
		Exceptions:
			Raises:
				TypeError - if the provided component is not an instnace of the Field class. 
		'''
		assert isinstance(component,Field),TypeError('The component argument shall be an instance of the Field class.')
		
		self.__template.add(component)
		return None
	
	@property
	def product(self):
		'''
		Goal: provide the result/product of the built, and reset the builder.
		Actions:
			Return a built Template instance and reset the Builder to the initial state.
		Returns: built_field:Template
		Exceptions:
			Raises:
				NotImplementedError - in case if the __field attribute hasn't been initialized - thus the construction hasn't started yet. 
		'''
		assert isinstance(self.__template,Template), NotImplementedError('The Builder has not fully initialized - thus the construction hasn\'t begun.')
		built_template=self.__template
		self.__reset()
		return built_template