from chathouse.utilities.security.validation.data.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field import Field


def create_a_template():

	'''
	Goal: create a template for validating incoming data, aimed at the POST /api/tokens/confirmation.
	Actions:
		Using the TemplateBuilder class - create an instance of PostConfirmationTemplateBuilder.
		Add neccessary fields with proper requirement: action - refers to a goal the requester tries to achieve, which needs the confirmation -> thus actions are delete(terminate) or put(reset).
		Return the instance of the Template class from the builder.
	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - template.
	
	Exceptions:
		Raises:
			ValueError - if the provided route argument doesn't fall under any of the alternative values.
	'''
	
	PostConfirmationTemplateBuilder=TemplateBuilder()
	PostConfirmationTemplateBuilder.add(Field('action',regex='^(?:delete|put)$',data_type=str))
	
	return PostConfirmationTemplateBuilder.template
