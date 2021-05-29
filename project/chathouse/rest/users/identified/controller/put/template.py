from chathouse.utilities.security.validation.data.template.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field.builder import FieldBuilder
from chathouse.utilities.security.validation.data.requirement import Nested,String,DataType


def create_a_template():

	'''
	Goal: create a template for validating data , depending on the initial request, aimed at the PUT /api/users/<identification>.

	Actions:
		According to the BuilderPattern proceed to build the Fields and the Template:
			Using the TemplateBuilder class - create an instance of PutIdentifiedUserTemplateBuilder.
			Using the FieldBuilder class - create an instance of PutIdentifiedUserFieldBuilder.

		Build a ResetField - set proper requisites, using a Nested requirement, provide nested (key:Requiremnt)s:
			password : a Nested requirement, shall contain (key:Requiremnt)s:
				current: with String Requirement of 64 characters - sha256 hexdigested;
				new: with String Requirement of 64 characters - sha256 hexdigested;
			private_key : a Nested requirement, shall contain (key:Requiremnt)s:
				iv: with DataType Requirement of a string;
				data: with DataType Requirement of a string.


		Return the instance of the Template class from the builder, thus reseting the PutIdentifiedUserTemplateBuilder.

	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - product.
	'''
	
	PutIdentifiedUserTemplateBuilder=TemplateBuilder()
	PutIdentifiedUserFieldBuilder=FieldBuilder()
	
	nested_requirement=Nested(**{
		'password':Nested(**{
			'current':String('^\w{64}$'),
			'new':String('^\w{64}$')
		}),
		'private_key':Nested(**{
			'iv':DataType(str),
			'data':DataType(str)
		})
	})

	PutIdentifiedUserFieldBuilder.requisites={'key':'reset','required':True}
	PutIdentifiedUserFieldBuilder.add(nested_requirement)
	PutIdentifiedUserTemplateBuilder.add(PutIdentifiedUserFieldBuilder.product)

	return PutIdentifiedUserTemplateBuilder.product