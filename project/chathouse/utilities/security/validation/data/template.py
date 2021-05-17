from chathouse.utilities.security.validation.data.field import Field

class Template:
	def __init__(self):
		self.__fields,self.__data={},{}

	def add(self,field):
		assert isinstance(field,Field), TypeError('Class of a field argument must be a subclass of the Field class.')
		self.__fields.update({field.key:field})

	def validate(self,**data):
		'''
		data may include non expecting fields, template must ignore them - store the requested ones.
		'''
		for key in self.__fields:
			if (value:=data.get(key,None)) is not None and self.__fields[key].validate(value): 
				self.__data[key]=value
			else:
				return False
		return len(self.__data)==len(data)
		
	@property
	def data(self):
		data=self.__data.copy()
		self.__data.clear()
		return data
	