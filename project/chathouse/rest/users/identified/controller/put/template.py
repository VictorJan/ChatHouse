from chathouse.utilities.security.validation.data.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field import Field


def create_a_template():

	'''
	Goal: create a template for validating data , depending on the initial request, aimed at the PUT /api/users/<identification>.

	Actions:
		Using the TemplateBuilder class - create an instance of PutIdentifiedUserTemplateBuilder.
		Add neccessary fields "current_password","new_password" with proper requirements : strings of at least 64 characters long - expecting hex digest of sha256. 	
		Add a neccessary field "private_key" with proper requirements : a dictionary with following structure of keys and datatypes:
			{
				iv:<str>,
				data:<str>
			}
		Return the instance of the Template class from the builder, thus reseting the PutIdentifiedUserTemplateBuilder.

	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - template.
	'''
	
	PutIdentifiedUserTemplateBuilder=TemplateBuilder()
	PutIdentifiedUserTemplateBuilder.add(Field('current_password',regex='^\w{64}$',data_type=str))
	PutIdentifiedUserTemplateBuilder.add(Field('new_password',regex='^\w{64}$',data_type=str))
	
	required_keys_n_types={'iv':str,'data':str}

	PutIdentifiedUserTemplateBuilder.add(Field('private_key',keys=required_keys_n_types,data_type=dict))

	return PutIdentifiedUserTemplateBuilder.template