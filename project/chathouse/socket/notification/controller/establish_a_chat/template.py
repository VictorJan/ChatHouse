from chathouse.utilities.security.validation.data.template.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field.builder import FieldBuilder
from chathouse.utilities.security.validation.data.requirement import DataType,String


def create_a_template():

	'''
	Goal: create a template for validating data , depending on the initial event, aimed at the /notification [establish_a_chat].

	Actions:
		According to the BuilderPattern proceed to build the Fields and the Template:
			Using the TemplateBuilder class - create an instance of Establish_a_ChatTemplateBuilder.
			Using the FieldBuilder class - create an instance of Establish_a_ChatFieldBuilder.

		1.Build the NameField - set proper requisites, using the String Requirement, providing the required regular expresion, and lastly build the product - reseting the Builder,for the next Field.
		Then add the built product/Field to the template , using Establish_a_ChatTemplateBuilder;
		[Note regular expression - a string of at least 4 characters/spaces long , 30 characters/spaces max and with at least 4 characters in it]

		2.Build the Participant_IdField - set proper requisites(required=False), using the DataType Requirement, providing the required datatype - int, and lastly build the product - reseting the Builder,for the next Field.
		Then add the built product/Field to the template , using Establish_a_ChatTemplateBuilder;
		[Note - the latter field - "participant_id" is set up as non required, due to the permitions to start chats without any participants]

		Return the instance of the Template class from the builder, thus reseting the Establish_a_ChatTemplateBuilder.

	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - product.
	'''
	Establish_a_ChatTemplateBuilder=TemplateBuilder()
	Establish_a_ChatFieldBuilder=FieldBuilder()
	
	Establish_a_ChatFieldBuilder.requisites={'key':'name','required':True}
	Establish_a_ChatFieldBuilder.add(String('^(?=.*(?:\w.*){4,})[\w\s]{4,30}$'))
	Establish_a_ChatTemplateBuilder.add(Establish_a_ChatFieldBuilder.product)

	Establish_a_ChatFieldBuilder.requisites={'key':'participant_id','required':False}
	Establish_a_ChatFieldBuilder.add(DataType(int))
	Establish_a_ChatTemplateBuilder.add(Establish_a_ChatFieldBuilder.product)

	return Establish_a_ChatTemplateBuilder.product