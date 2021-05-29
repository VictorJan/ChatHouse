from chathouse.utilities.security.validation.data.template.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field.builder import FieldBuilder
from chathouse.utilities.security.validation.data.requirement import String


def create_a_template():

	'''
	Goal: create a template for validating incoming data, aimed at the POST /api/tokens/confirmation.
	Actions:
		According to the BuilderPattern proceed to build the Fields and the Template:
			Using the TemplateBuilder class - create an instance of PostConfirmationTemplateBuilder.
			Using the FieldBuilder class - create an instance of PostConfirmationFieldBuilder.

		1.Build the ActionField - set proper requisites, using the String Requirement, providing the required regular expresion, and lastly build the product - reseting the Builder,for the next Field.
		Then add the built product/Field to the template , using PostConfirmationTemplateBuilder;
		[Note: action - refers to a goal the requester tries to achieve, which needs the confirmation -> thus actions are delete(terminate) or put(reset)]
		
		2.Return the instance of the Template class from the builder, thus reseting the PostGrantTemplateBuilder.
	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - product.
	'''
	
	PostConfirmationTemplateBuilder=TemplateBuilder()
	PostConfirmationFieldBuilder=FieldBuilder()
	
	PostConfirmationFieldBuilder.requisites={'key':'action','required':True}
	PostConfirmationFieldBuilder.add(String('^(?:delete|put)$'))
	PostConfirmationTemplateBuilder.add(PostConfirmationFieldBuilder.product)

	return PostConfirmationTemplateBuilder.product
