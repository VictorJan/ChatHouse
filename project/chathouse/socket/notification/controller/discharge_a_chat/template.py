from chathouse.utilities.security.validation.data.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field import Field


def create_a_template():

	'''
	Goal: create a template for validating data , depending on th initial event, aimed at the /notification [discharge_a_chat].

	Actions:
		Using the TemplateBuilder class - create an instance of Discharge_a_ChatTemplateBuilder.
		Add a neccessary field "id" with proper requirements : an integer. 
		Return the instance of the Template class from the builder, thus reseting the Discharge_a_ChatTemplateBuilder.

	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - template.
	'''
	
	Discharge_a_ChatTemplateBuilder=TemplateBuilder()
	Discharge_a_ChatTemplateBuilder.add(Field('id',data_type=int))
	
	return Discharge_a_ChatTemplateBuilder.template