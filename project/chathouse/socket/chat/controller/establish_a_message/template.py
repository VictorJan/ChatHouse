from chathouse.utilities.security.validation.data.template.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field.builder import FieldBuilder
from chathouse.utilities.security.validation.data.requirement import Nested,DataType


def create_a_template():

	'''
	Goal: create a template for validating data , depending on the initial event, aimed at the /chat [establish_a_message].

	Actions:
		According to the BuilderPattern proceed to build the Fields and the Template:
			Using the TemplateBuilder class - create an instance of Establish_a_ChatTemplateBuilder.
			Using the FieldBuilder class - create an instance of Establish_a_ChatFieldBuilder.

		Build a ContentField - set proper requisites, using a Nested requirement, provide nested (key:Requiremnt)s:
			iv: with DataType Requirement of a string;
			data: with DataType Requirement of a string.

		[Note] - the content of the message - has to be encrypted, so it shall follow the latter structure - thus the backend is not able to decrypt the content.
		Therefore in order to accept only properly formed messages,keeping the integrity and the confidentiality intact - the mentioned structure is a set up as a guideline.

		Return the instance of the Template class from the builder, thus reseting the Establish_a_MessageTemplateBuilder.

	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - product.
	'''
	
	Establish_a_MessageTemplateBuilder=TemplateBuilder()
	Establish_a_MessageFieldBuilder=FieldBuilder()
	
	nested_requirement=Nested(**{
		'iv':DataType(str),
		'data':DataType(str)
	})

	Establish_a_MessageFieldBuilder.requisites={'key':'content','required':True}
	Establish_a_MessageFieldBuilder.add(nested_requirement)
	Establish_a_MessageTemplateBuilder.add(Establish_a_MessageFieldBuilder.product)

	return Establish_a_MessageTemplateBuilder.product