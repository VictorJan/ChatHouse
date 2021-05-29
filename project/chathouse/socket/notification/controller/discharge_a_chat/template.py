from chathouse.utilities.security.validation.data.template.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field.builder import FieldBuilder
from chathouse.utilities.security.validation.data.requirement import DataType


def create_a_template():

	'''
	Goal: create a template for validating data , depending on the initial event, aimed at the /notification [discharge_a_chat].

	Actions:
		According to the BuilderPattern proceed to build the Fields and the Template:
			Using the TemplateBuilder class - create an instance of Discharge_a_ChatTemplateBuilder.
			Using the FieldBuilder class - create an instance of Discharge_a_ChatFieldBuilder.

		Build the IdField - set proper requisites, using the DataType Requirement, providing the required datatype - int, and lastly build the product - reseting the Builder.
		Then add the built product/Field to the template , using Discharge_a_ChatTemplateBuilder;
		
		Return the instance of the Template class from the builder, thus reseting the Discharge_a_ChatTemplateBuilder.

	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - product.
	'''
	Discharge_a_ChatTemplateBuilder=TemplateBuilder()
	Discharge_a_ChatFieldBuilder=FieldBuilder()

	Discharge_a_ChatFieldBuilder.requisites={'key':'id','required':True}
	Discharge_a_ChatFieldBuilder.add(DataType(int))
	Discharge_a_ChatTemplateBuilder.add(Discharge_a_ChatFieldBuilder.product)
	
	return Discharge_a_ChatTemplateBuilder.product