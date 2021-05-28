from chathouse.utilities.security.validation.data.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field import Field


def create_a_template():

	'''
	Goal: create a template for validating data , depending on the initial request, aimed at the DELETE /api/users/<identification>.

	Actions:
		Using the TemplateBuilder class - create an instance of DeleteIdentifiedUserTemplateBuilder.
		Add a neccessary field "password" with proper requirements : a string of at least 64 characters long - expecting hex digest of sha256. 	
		Return the instance of the Template class from the builder, thus reseting the PutIdentifiedUserTemplateBuilder.

	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - template.
	'''
	
	DeleteIdentifiedUserTemplateBuilder=TemplateBuilder()
	DeleteIdentifiedUserTemplateBuilder.add(Field('password',regex='^\w{64}$',data_type=str))
	
	return DeleteIdentifiedUserTemplateBuilder.template