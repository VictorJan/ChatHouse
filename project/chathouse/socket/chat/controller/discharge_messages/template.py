from chathouse.utilities.security.validation.data.template.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field.builder import FieldBuilder
from chathouse.utilities.security.validation.data.requirement import Iterable


def create_a_template():

	'''
	Goal: create a template for validating data , depending on the initial event, aimed at the /chat [discharge_messages].

	Actions:
		According to the BuilderPattern proceed to build the Fields and the Template:
			Using the TemplateBuilder class - create an instance of Discharge_MessagesTemplateBuilder.
			Using the FieldBuilder class - create an instance of Discharge_MessagesFieldBuilder.
		
		Build the MessagesField - set proper requisites, using the Iterable Requirement, providing the required iterable datatype - list and internal datatype - int, and lastly build the product - reseting the Builder.
		Then add the built product/Field to the template , using Discharge_MessagesTemplateBuilder;
		
		Add a neccessary field "messages" with proper requirements : a list of inner values:int.

		Return the instance of the Template class from the builder, thus reseting the Discharge_MessagesTemplateBuilder.

	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - product.
	'''
	
	Discharge_MessagesTemplateBuilder=TemplateBuilder()
	Discharge_MessagesFieldBuilder=FieldBuilder()

	Discharge_MessagesFieldBuilder.requisites={'key':'messages','required':True}
	Discharge_MessagesFieldBuilder.add(Iterable(list,int))
	Discharge_MessagesTemplateBuilder.add(Discharge_MessagesFieldBuilder.product)

	return Discharge_MessagesTemplateBuilder.product