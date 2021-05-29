from chathouse.utilities.security.validation.data.field import Field

class Template:
	'''
	Goal: Class Template - is meant to be used as a part of a Builder Pattern.
	Thus the instances of the class shall only be used with the TemplateBuilder class - which performs the construction of the Template.
	'''
	def __init__(self):
		'''
		Goal:initialize a Template instance with empty fields and data - thus requiring to build the Template, by adding Fields.
		Returns: None
		'''
		self.__fields,self.__data={},{}
		return None

	def add(self,field):
		'''
		Goal:add a field to a template instance.
		Arguments: field:Field.
		Actions: having received the Field instance , update the current fields with incoming instance, assinging it to a respective self established key.
		Exceptions:
			Raises:
				TypeError - if the sumbitted <field> is not an instance of the Field class.
		'''
		assert isinstance(field,Field), TypeError('Class of a field argument must be a subclass of the Field class.')
		self.__fields.update({field.key:field})

	def validate(self,**payload):
		'''
		Goal: validate incoming data against the injected fields.
		Arguments:data - key word argument.
		Actions:
			First, iterate through all established fields -> based on a key of the field - find payload from the data according to the key.
			If there is data related to the key and validation performed by the respective Field instance has been successful:
				Assign the validated value to the product data according to the key.
			Otherwise, at this point such key,value pair wasn't found or the data was invalid according tot he Field instance.
			[!However!] The Field itself could be required or not required , so the next step is to verify:
			If the Field is required:
				return False - informing that the validation hasn't been successful.
			Otherwise proceeed to the next iteration step.

			Having validated each inserted field - what's left is to verify that the provided payload didn't contain any unnecessary key/value pairs.
			This is done by making sure, that the length of the product dictionary is equal to the initial payload.

		Returns True|False - establishing the validity of the initial payload.
		'''
		for key in self.__fields:
			if (value:=payload.get(key,None)) is not None and self.__fields[key].validate(value): 
				self.__data[key]=value
			elif self.__fields[key].required:
				return False
		return len(self.__data)==len(payload)
		
	@property
	def data(self):
		'''
		Goal: return the product of the validation process - stored data. Thus , this resets the Template to be used again.
		Returns: data:dict -product of the validation
		[Note in order to correctly export the data and not lose it  - this requires shallow copying.]
		'''
		data=self.__data.copy()
		self.__data.clear()
		return data
	