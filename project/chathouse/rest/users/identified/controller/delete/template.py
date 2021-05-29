from chathouse.utilities.security.validation.data.template.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field.builder import FieldBuilder
from chathouse.utilities.security.validation.data.requirement import String

def create_a_template():

	'''
	Goal: create a template for validating data , depending on the initial request, aimed at the DELETE /api/users/<identification>.

	Actions:
		According to the BuilderPattern proceed to build the Fields and the Template:
			Using the TemplateBuilder class - create an instance of DeleteIdentifiedUserTemplateBuilder.
			Using the FieldBuilder class - create an instance of DeleteIdentifiedUserFieldBuilder.

		Build the PasswordField - set proper requisites, using the String Requirement, providing the required regular expresion, and lastly build the product - reseting the Builder.
		Then add the built product/Field to the template , using DeleteIdentifiedUserTemplateBuilder;
		[Note regular expression - a string of 64 characters - the sha256 hexdigested hash]

		Add a neccessary field "password" with proper requirements : a string of at least 64 characters long - expecting hex digest of sha256. 	
		Return the instance of the Template class from the builder, thus reseting the DeleteIdentifiedUserTemplateBuilder.

	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - product.
	'''
	
	DeleteIdentifiedUserTemplateBuilder=TemplateBuilder()
	DeleteIdentifiedUserFieldBuilder=FieldBuilder()
	
	DeleteIdentifiedUserFieldBuilder.requisites={'key':'password','required':True}
	DeleteIdentifiedUserFieldBuilder.add(String('^\w{64}$'))
	DeleteIdentifiedUserTemplateBuilder.add(DeleteIdentifiedUserFieldBuilder.product)
	
	return DeleteIdentifiedUserTemplateBuilder.product