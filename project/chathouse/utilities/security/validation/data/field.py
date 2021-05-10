import re

class Field:
	def __init__(self,key,**requirements):
		assert isinstance(key,str), TypeError('The key argument has to be a string.')
		self.__key,self.__requirements=key,requirements

	def validate(self,data):
		contains=lambda key:self.__requirements.get(key,None)
		if (expr:=contains('regex')) and not re.fullmatch(expr,data):
			return False
		if (data_type:=contains('data_type')) and not isinstance(data,data_type):
			return False
		if (wrapper:=getattr(data,'__contains__',None)) is not None and (nested:=contains('contains')) and not tuple(filter(wrapper,iter((nested,))))==data:
			return False
		return True

	@property
	def key(self):
		return self.__key
	
