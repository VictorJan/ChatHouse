from chathouse.utilities.security.validation.data.requirement import Requirement

class Field:
	'''
	Field - a class meant to function as a tool for validating certain fields in bodies of incomming requests.

	Methods:
		add(self,requirement:Requirement) - meant to perform constructive behaviour , by appending requirements.
		validate(self,data) - meant to validate the provided data based on the implemented requirements.
	
	Attributes:
		__key - meant to store a key:str value , referencing a certain key in body of a certain request.
		__required - meant to store a required state of a Field instance.
		__requirements - meant to store a list of requirements, implemented into the Field instance.
	
	Properties:
		key - returns the __key attribute
		required - returns the __required attribute
	'''
	def __init__(self,key,required=True):
		'''
		Goal: initialize a Field instance with a proper key, a requirement state.
		Arguments: key:str, required:bool(default=True).
		Exceptions:
			Raises:
				TypeError - in cases when the datatype for the key argument is not a string or the required state value wasn't a boolean.
		Returns: None.
		'''
		
		assert isinstance(key,str), TypeError('The key argument has to be a string.')

		assert isinstance(required,bool), TypeError('The required argument has to be a boolean.')
		
		self.__key,self.__required,self.__requirements=key,required,[]

		return None

	def add(self,requirement):
		'''
		Goal: execute the constructive behaviour/features, by injecting/adding/appending requirements to the Field instance.
		Arguments: requirement:Requirement.
		Returns:None.
		Exceptions:
			Raises:
				TypeError - if the provided requirement argument is not an instance of the Requirement class.
		'''
		assert isinstance(requirement,Requirement), TypeError('The requirement argument shall be - an instance of the Requirement class.')
		self.__requirements.append(requirement)

	def validate(self,data):
		'''
		Goal: perform the validation for the initialized Field.
		Arguments: data:*.
		Actions:
			Go through each of the implemented requirements and execute respective validation , passing the incoming data.
			If at any case , the validation has determined the data as invalid - the whole validation fails.
			Thus the validation returns True. Otherwise , if the iteration has gone through all requirements and hasn't found any invalid case - returns True
			[Note in some instances - this would perform a certain chain of validation , in case of using Nested Requirements]
		Returns: True|False. 
		'''
		return not any ( True for requirement in self.__requirements if not requirement.validate(data) )


	@property
	def key(self):
		'''
		Goal: return the key assigned to the field instance.
		Returns: innner key:str.
		'''
		return self.__key

	@property
	def required(self):
		'''
		Goal: return the required state assigned to the field instance.
		Returns: innner required:bool.
		'''
		return self.__required