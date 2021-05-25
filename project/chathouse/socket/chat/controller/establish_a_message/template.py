from chathouse.utilities.security.validation.data.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field import Field


def create_a_template():

	'''
	Goal: create a template for validating data , depending on th initial event, aimed at the /chat [establish_a_message].

	Actions:
		Using the TemplateBuilder class - create an instance of Establish_a_MessageTemplateBuilder.
		Add a neccessary field "content" with proper requirements : a dictionary with following structure of keys and datatypes:
			{
				iv:<str>,
				data:<str>
			}
		[Note] - the content of the message - has to be encrypted, so it shall follow the latter structure - thus the backend is not able to decrypt the content.
		Therefore in order to accept only properly formed messages,keeping the integrity and the confidentiality intact - the mentioned structure is a set up as a guideline.

		Return the instance of the Template class from the builder, thus reseting the Establish_a_MessageTemplateBuilder.

	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - template.
	'''
	
	Establish_a_MessageTemplateBuilder=TemplateBuilder()
	Establish_a_MessageTemplateBuilder.add(Field('content',data_type=dict,keys={'iv':str,'data':str}))
	return Establish_a_MessageTemplateBuilder.template