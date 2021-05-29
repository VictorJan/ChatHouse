from abc import ABC,abstractmethod
import re

class Requirement(ABC):
	'''
	Class Requirement - abstract class meant to implement requirement functionalities (such as validation) for the Field instances.
	Inherits: ABC.
	methods:
		validate(self,data):
			Goal:shall provide an application of a certain validation.
	'''

	@abstractmethod
	def validate(self,data):
		pass

class DataType(Requirement):
	'''
	DataType - a class meant to implement type validation for a provided type instance.
	Inherits: Requirement.

	Attributes:
		__value:type - meant to store the inner provided type instance.

	Methods:
		validate - executes the implementation of respective validation.
	'''
	def __init__(self,value):
		'''
		Goal: initialize an istance of a DataType requirement - providing a data type instance.
		Arguments: value:type.
		Returns:None.
		Exceptions:
			Raises:
				TypeError - if the provided value argument is not a type.
		'''
		assert isinstance(value,type), TypeError('The value argument shall be an instance of "type".')
		self.__value=value

	def validate(self,data):
		'''
		Goal: perform a datatype validation process based on the provided data.
		Arguments:data:*.
		Returns: True|False:bool.
		'''
		return isinstance(data,self.__value)


class String(Requirement):
	'''
	String - a class meant to implement string validation based on the matching.
	Inherits: Requirement.

	Attributes:
		__regex:str - meant to store a regual expresion for the full match validation.
		__datatype:DataType(str) - meant to store an predecided DataType of incoming data.

	Methods:
		validate - executes the implementation of respective validation.
	'''
	def __init__(self,regex):
		'''
		Goal: initialize an istance of a String requirement - providing a regual expresion string.
		Arguments: regex:str.
		Returns:None.
		Exceptions:
			Raises:
				TypeError - if the provided regex argument is not a string.
		'''
		assert isinstance(regex,str), TypeError('The regex argument shall be an instance of "str".')
		self.__regex = regex
		self.__datatype = DataType(str)

	def validate(self,data):
		'''
		Goal: perform a string validation process based on the provided data.
		Arguments:data:*.
		Actions:
			1.Validate the datatype - using the inner datatype attribute.
			2.Find a full match of provided data ,based on the initialized regular expression. 
		Returns: True|False:bool.
		'''
		return self.__datatype.validate(data) and re.fullmatch(self.__regex,data)



class Iterable(Requirement):
	'''
	Iterable - a class meant to implement validation of an iterable instance , based on the provided datatype.
	Inherits:Requirement.

	Attributes:
		__datatype:DataType(iterable datatype) - inner DataType Requirement, initialized with a respetive datatype value of an iterable.
		__internal_datatype:DataType(datatype)|None - inner DataType Requirement, initialized to validate datatype values of inner instances | None. (Optional)

	Methods:
		validate - executes the implementation of respective validation.
	'''
	def __init__(self,datatype,internal_datatype=None):
		'''
		Goal: initialize an istance of an Iterable requirement - providing an iterable data type and (optional) internal data type value.
		Arguments: datatype:type, inner_datatype:type|None.
		Returns:None.
		Exceptions:
			Raises:
				TypeError - if the provided value argument is not a type.
		'''
		assert isinstance(datatype,type) and hasattr(datatype,'__iter__'), TypeError('The datatype argument shall be of type instance and contanin an appropriate iter dunder method - thus be iterable.')
		assert isinstance(internal_datatype,type) if internal_datatype is not None else True, TypeError('The internal_datatype argument shall an instance of "type".')
		
		self.__datatype = DataType(datatype)
		self.__internal_datatype = DataType(internal_datatype) if internal_datatype is not None else None

	def validate(self,data):
		'''
		Goal: perform an iterable validation process based on the provided data.
		Arguments:data:*.
		Actions:
			1.Validate the datatype - using the inner datatype attribute.
			2.If the internal datatype has been provided - verify the datatype of each item based on the internal datatype
		Returns: True|False:bool.
		'''

		return self.__datatype.validate(data) and (data and all(map(lambda item: self.__internal_datatype.validate(item) ,data)) if self.__internal_datatype is not None else True)

class Nested(Requirement):
	'''
	Nested - a class meant to implement a nested validation process.
	
	Inherits:Requirement

	Attributes:
		__payload - meant to store the nesting payload with a proper structure : Each provided key:str must contain only one value, which has to be an instance of Requirement class/subclass.
		__datatype:DataType(dict) - inner DataType Requirement, initialized with a dictionary type.

	'''
	def __init__(self,**payload):
		'''
		Goal: initialize an istance of a String requirement - providing a properly constructed nested payload - for further validation.
		Arguments: payload:dict - key-word-argument , a nested payload of requirements - that shall follow the guildelines: each key:str must only contain a value of Requirement class/subclass.
		Returns:None.
		Exceptions:
			Raises:
				TypeError - if the provided payload doesn't follow the proper structure/guidelines - key:str : value:Requirement.
		'''

		assert payload and isinstance(payload,dict) and all(map(lambda key: isinstance(key,str) and isinstance(payload[key],Requirement) ,payload)), ValueError('The payload, key word argument shall not be empty, must contain keys:str with values:Requirement')

		self.__payload=payload
		self.__datatype=DataType(dict)


	def validate(self,data):
		'''
		Goal: perform a validation of the provided data based on the proper payload of requirements.
		Arguments:data:dict.
		Actions:
			1.Validate the datatype - using the inner datatype attribute.
			2.Make sure of the equal amount of shallow keys.
			3.Iterating through the required keys in the payload , verify the existance of each of them and proceed to execute validation according to the assigned Requirements value.
			If at any point the provided data either didn't contain a required key or the assigned Requirement failed to validate the value from the data, according to that key -> whole validation fails.
			Thus returns False, otherwise True.
		Returns: True|False:bool.
		'''
		return self.__datatype.validate(data) and len(data)==len(self.__payload) and ( not any( True for key in self.__payload if (value:=data.get(key,None)) is None or not self.__payload[key].validate(value) ) ) 