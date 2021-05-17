import re
import copy


class Field:
	def __init__(self,key,**requirements):
		
		resolve_data_type=lambda key: str if key == 'regex' else type if key =='data_type' else dict

		assert isinstance(key,str), TypeError('The key argument has to be a string.')

		assert all(map(lambda key: key in ('regex','data_type','keys') and isinstance(requirements[key],resolve_data_type(key)) ,requirements)), ValueError('Allowed requirements are regex:str , data_type:type and keys:dict.')

		assert (self.__properly_nested(copy.deepcopy(payload),True) if (payload:=requirements.get('keys')) else True), ValueError('Allowed requirements are regex:str , data_type:type and keys:dict.')

		self.__key,self.__requirements=key,requirements

	def validate(self,data):
		
		contains=lambda key:self.__requirements.get(key,None)

		if (data_type:=contains('data_type')) and not isinstance(data,data_type):
			return False
		if (expr:=contains('regex')) and not re.fullmatch(expr,data):
			return False
		if (required_keys:=contains('keys')) and isinstance(required_keys,dict) and data_type==dict and not self.__search(data,copy.deepcopy(required_keys),True):
			return False
		
		return True

	@staticmethod
	def __search(incoming,required,valid):
		'''
		Goal: validate the nested payload based on the 'keys' requirement.
		Arguments: incoming:dict, required:dict, valid:bool.
		Actions: Using recursion get each nested required key and a required data type / content , and validate the incoming against it.
			search:
				If the required payload is a dictionary and everything seems to be valid ->:
					Pop an item pair from the required payload : a (current) required key , a (current) required content. 
					If there is no required key in the keys of the incoming data or the datatype of the incoming[requreired key] is not the same as the datatype of the required content , return False.
					Otherwise keys seems to match ,so resume with the next steps:
						If there is more nested required data - the required content is a dictionary itself - perform the search deeper , by searching the incoming[required key] and validating it against the required_content.
					Having compared the values and data types, and verified if there is a need to search deeper:
					If at this point the state of validity hasn't changed from it's core True state and there is still some required data,search the rest of the incoming payload, and compare it against what have been left of the required data.
					Otherwise proceed to return the current state of validity.
		Returns: valid:bool.
		'''
		if isinstance(required,dict) and valid:
			currently_required_key,currently_required_content=required.popitem()
			
			if (nested_data:=incoming.get(currently_required_key,None)) is None or not (isinstance(nested_data,currently_required_content if isinstance(currently_required_content,type) else type(currently_required_content)) ):
				return False

			elif isinstance(currently_required_content,dict):
				valid=Field.__search(nested_data,currently_required_content,valid)
			
			valid=Field.__search(incoming,required,valid) if valid and required else valid

		return valid

	@staticmethod
	def __properly_nested(payload,valid):
		'''
		Goal: validate the requiremet's payload based on the Proper structure.
		Arguments: payload:dict, valid:bool.
		Proper structure: each key shall only contain a data type or another dictionary , that follows the same rules. In other words : payload = { key : <data type|{key:...,...}> , key : ... }
		Actions: Using recursion get each proposed nested required key and a required data type / content , and validate it against the Proper structure.
			search:
				If the required payload is a dictionary and everything seems to be valid ->:
					Pop an item pair from the required payload : a (current) required key , a (current) required content , store it in a requirement tuple with respected indexes. 
					If there is no required key is not a string or the datatype of the required datatype/content is neither a type or a dictionary , return False.
					Otherwise a datatype of the key and the nested requirement seems to be valid ,so resume with the next steps:
						If there is more nested required data - the required content is a dictionary itself - perform the search deeper , by validating the required content , or requirement[1].
					Having compared the data types, and verified if there is a need to search deeper:
					If at this point the state of validity hasn't changed from it's core True state and there is still some required data, search the rest of the proposed required data.
					Otherwise proceed to return the current state of validity.
		Returns: valid:bool.
		'''
		if isinstance(payload,dict) and valid:

			requirement=(requirement:=payload.popitem())
			if not isinstance(requirement[0] ,str) or not any(map(lambda dt: isinstance(requirement[1],dt) ,(dict,type))):
				return False

			elif isinstance(requirement[1],dict):
				valid=Field.__properly_nested(requirement[1],valid)

			valid = Field.__properly_nested(payload,valid) if valid and payload else valid

		return valid

		

	@property
	def key(self):
		return self.__key
	
