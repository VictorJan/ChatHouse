from chathouse.utilities.security.validation.data.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field import Field


def create_a_template():

	'''
	Goal: create a template for validating data , depending on th initial event, aimed at the /chat [discharge_messages].

	Actions:
		Using the TemplateBuilder class - create an instance of Discharge_MessagesTemplateBuilder.
		Add a neccessary field "messages" with proper requirements : a list of inner values:int.

		Return the instance of the Template class from the builder, thus reseting the Discharge_MessagesTemplateBuilder.

	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - template.
	'''
	
	Discharge_MessagesTemplateBuilder=TemplateBuilder()
	Discharge_MessagesTemplateBuilder.add(Field('messages',data_type=list,inner_data_type=int))
	return Discharge_MessagesTemplateBuilder.template