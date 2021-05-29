from chathouse.utilities.security.validation.data.template.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field.builder import FieldBuilder
from chathouse.utilities.security.validation.data.requirement import String,Nested,DataType


def create_a_template(route):

	'''
	Goal: create a template for validating data , depending on th initial route,  in the post requests aimed at the /api/tokens/grant.

	Actions:
		According to the BuilderPattern proceed to build the Fields and the Template:
			Using the TemplateBuilder class - create an instance of PostGrantTemplateBuilder.
			Using the FieldBuilder class - create an instance of PostGrantFieldBuilder.
		
		1.Build the PasswordField - set proper requisites, using the String Requirement, providing the required regular expresion, and lastly build the product - reseting the Builder,for the next Field.
		Then add the built product/Field to the template , using PostGrantTemplateBuilder;
		[Note regular expression - a string of 64 characters - the sha256 hexdigested hash]

		If the route is signup:
			2.Build the KeyringField - set:
				Create a 2 Nested Requirements:
				1)First Nested requirement shall contain (key:Requiremnt)s :
					public_key : with DataType Requirement of an integer;
					g: with DataType Requirement of an integer;
					m: with DataType Requirement of an integer;
				private_key : 2) Second Nested requirement, shall contain (key:Requiremnt)s:
					iv: with DataType Requirement of a string;
					data: with DataType Requirement of a string.


		Return the instance of the Template class from the builder, thus reseting the PostGrantTemplateBuilder.

	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - product.
	
	Exceptions:
		Raises:
			ValueError - if the provided route argument doesn't fall under any of the alternative values.
	'''
	
	assert any(map(lambda a: route==a,('signup','login'))), ValueError('The route argument shall have a value of "signup" or "login".')

	PostGrantTemplateBuilder=TemplateBuilder()
	PostGrantFieldBuilder=FieldBuilder()
	
	PostGrantFieldBuilder.requisites={'key':'password','required':True}
	PostGrantFieldBuilder.add(String('^\w{64}$'))
	PostGrantTemplateBuilder.add(PostGrantFieldBuilder.product)
	
	if  route=='signup':
		
		nested_requirement=Nested(**{
			'public_key':DataType(int),
			'g':DataType(int),
			'm':DataType(int),
			'private_key':Nested(**{
				'iv':DataType(str),
				'data':DataType(str)
			})
		})

		PostGrantFieldBuilder.requisites={'key':'keyring','required':True}
		PostGrantFieldBuilder.add(nested_requirement)
		PostGrantTemplateBuilder.add(PostGrantFieldBuilder.product)

	return PostGrantTemplateBuilder.product