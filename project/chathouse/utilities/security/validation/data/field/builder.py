from chathouse.utilities.security.validation.data.builder import Builder
from chathouse.utilities.security.validation.data.field import Field
from chathouse.utilities.security.validation.data.requirement import Requirement

class FieldBuilder(Builder):
	'''
	FieldBuilder - a class meant to implement contructive and productive functionalities aimed at the Field instances.
	Inherits: ABC.
	Flow:
		1.Initialize an empty FieldBuilder -> which calls the __reset;
		[1.2.The call to __reset - sets up inital __field and __requisites attribute to None_s.]
		2.Set the requisites(key:str,required:bool) for the future Field product -> which calls __start;
		[2.2.The call to __start - begins the production, by initializing the Field instance with the set up requisites;]
		3.Perform construction - add components - Requirement_s.
		4.To end the construction stage, use the product property, which retreives the built Field instance and resets the Builder to the initial step, using the __reset call.
	
	Methods:
		__reset(self) - sets the Builder to the initial state, which would require the proper requisites, to begin the construction process.
		__start(self) - begins the construcion process -> thus fully initializing the Builder.
		add(self,component) - executes contruction capabilities, providing the Requirement instances as components of the Field.

	Properties:
		Getters:
			product - provide a result of the contruction, containing productive features, and set the builder to the initial state.
			requisites - provide the initialized requisites, used to start the building process.
		Setters:
			product - set the requisites attribute , according to the guidelines, which would begin the construction, fully intializing the Builder.
	'''
	
	def __init__(self):
		'''
		Goal: partly initialize the Builder, by setting it to the initial state - using the reset call.
		Returns:None 
		'''
		self.__reset()

	def __reset(self):
		'''
		Goal: sets the Builder to the initial state - requiring requisites to start the construction.
		Action: set the __requisites and __field to None_s.
		Returns:None.
		'''
		self.__requisites=None
		self.__field=None
		return None

	def __start(self):
		'''
		Goal: begin the construction/bulding process - by initializing the Field instance with proper requisites -> thus fully initializing the Builder.
		[Note: according to the Flow - this call will only be initiated when the requisites.However, for the future implementations and common knowledge - raise the respective exceptions, if requisites haven't been established.]
		Actions: initialize a Field instance with established requisites, and assing the instance to the __field attribute. 
		Returns:None
		Exceptions:
			Raises:
				NotImplementedError -  if requisites haven't been established yet.
		'''
		assert isinstance(self.__requisites,dict), NotImplementedError('The requisites haven\'t been set up, the contruction can\'t be initiated.')
		self.__field=Field(**self.__requisites)
		return None

	def add(self,component):
		'''
		Goal: execute a part of the construction/building process - component injection.
		Arguments: component:Requirement.
		Actions:
			Adds a Requirement to the initialized Field.
		Returns None.
		Exceptions:
			Raises:
				NotImplementedError - if the Field instance is not set up yet - the constuction/building process hasn't been properly started.
				TypeError - if the provided component is not an instnace of the Requirement class/subclass. 
		'''
		assert isinstance(self.__field,Field), NotImplementedError('The Field instance hasn\'t been set up yet, thus the construction process is denied.')
		assert isinstance(component,Requirement),TypeError('The component argument shall be an instance of the Field class.')
		
		self.__field.add(component)
		return None


	@property
	def requisites(self):
		'''
		Goal: retreive the __requisites attribute, which have been used to initialize the Field instance.
		Returns:__requisites:dict.
		'''
		return self.__requisites
	
	@requisites.setter
	def requisites(self,other):
		'''
		Goal: set the values for the __requisites attribute , according to the guidelines and begin the construction/manufacturing process of the Builder.
		Arguments: other:dict.
		Actions: If no exceptions has been raised - set the __requisites to the provided other argument and begin the construction , by calling the __start.
		Returns:None.
		Exceptions:
			Raises:
				ValueError - if the provided other agrument doesn't follow the integrated guidelines.
		'''
		guidelines = (('key',str),('required',bool))
		assert isinstance(other,dict) and len(other)==len(guidelines) and all(map(lambda requisite: (value:=other.get(requisite[0],None)) is not None and isinstance(value,requisite[1]) ,guidelines)),\
		ValueError('The requisites shall only be set to a dictionary containing keys : key:str and required:bool.')

		self.__requisites=other
		self.__start()

		return None
	
	@property
	def product(self):
		'''
		Goal: provide the result/product of the built, and reset the builder.
		Actions:
			Return a built Field instance and reset the Builder to the initial state.
		Returns: built_field:Field
		Exceptions:
			Raises:
				NotImplementedError - if the __field attribute hasn't been initialized - thus the construction hasn't started yet. 
		'''
		assert isinstance(self.__field,Field) and isinstance(self.__requisites,dict), NotImplementedError('The Builder has not fully initialized - thus the construction hasn\'t begun. Please set the requisites.')
		built_field=self.__field
		self.__reset()
		return built_field