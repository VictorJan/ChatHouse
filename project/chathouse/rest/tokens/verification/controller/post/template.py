from chathouse.utilities.security.validation.data.template.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field.builder import FieldBuilder
from chathouse.utilities.security.validation.data.requirement import String


def create_a_template(route):

	'''
	Goal: create a template based on the initial route of the requrest.
	Arguments: route:str , expecting alternatives = signup/login.
	Actions:
		According to the BuilderPattern proceed to build the Fields and the Template:
			Using the TemplateBuilder class - create an instance of PostVerificationTemplateBuilder.
			Using the FieldBuilder class - create an instance of PostVerificationFieldBuilder.
		If the route is signup:
			
			S.1.Build the EmailField - set proper requisites, using the String Requirement, providing the required regular expresion, and lastly build the product - reseting the Builder,for the next Field.
			Then add the built product/Field to the template , using PostVerificationTemplateBuilder;
			[Note regular expression - a proper email structure]

			S.2.Build the UsernameField - set proper requisites, using the String Requirement, providing the required regular expresion, and lastly build the product - reseting the Builder,for the next Field.
			Then add the built product/Field to the template , using PostVerificationTemplateBuilder;
			[Note regular expression - a username shall only contain word-characters, with a range of [6;30] characters long]

			S.3.Build the NameField - set proper requisites, using the String Requirement, providing the required regular expresion, and lastly build the product - reseting the Builder,for the next Field.
			Then add the built product/Field to the template , using PostVerificationTemplateBuilder;
			[Note regular expression - a name shall only contain letters, with a range of [3;25] characters long]
			
			S.4.Build the AboutField - set proper requisites, using the String Requirement, providing the required regular expresion, and lastly build the product - reseting the Builder,for the next Field.
			Then add the built product/Field to the template , using PostVerificationTemplateBuilder;
			[Note regular expression - an about shall at least contain 5 letters]
			
			S.5.Return the instance of the Template class from the builder, thus reseting the PostVerificationTemplateBuilder.
		Otherwise:
			L.1.Build the IdentificationField - set proper requisites, using the String Requirement, providing the required regular expresion, and lastly build the product - reseting the Builder,for the next Field.
			Then add the built product/Field to the template , using PostVerificationTemplateBuilder;
			[Note regular expression - a proper email structure or the username pattern]

			L.2.Return the instance of the Template class from the builder.
	
	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - product.
	
	Exceptions:
		Raises:
			ValueError - if the provided route argument doesn't fall under any of the alternative values.
	'''
	
	assert any(map(lambda a: route==a,('signup','login'))), ValueError('The route argument shall have a value of "signup" or "login".')



	PostVerificationTemplateBuilder=TemplateBuilder()
	PostVerificationFieldBuilder=FieldBuilder()
	if  route=='signup':
		
		PostVerificationFieldBuilder.requisites={'key':'email','required':True}
		PostVerificationFieldBuilder.add(String('^(?=[\w_\-\.]+\@\w+\.\w+)[\w_\-\.@]{5,60}$'))
		PostVerificationTemplateBuilder.add(PostVerificationFieldBuilder.product)

		PostVerificationFieldBuilder.requisites={'key':'username','required':True}
		PostVerificationFieldBuilder.add(String('^\w{6,30}$'))
		PostVerificationTemplateBuilder.add(PostVerificationFieldBuilder.product)
		
		PostVerificationFieldBuilder.requisites={'key':'name','required':True}
		PostVerificationFieldBuilder.add(String('^[a-zA-Z]{3,25}'))
		PostVerificationTemplateBuilder.add(PostVerificationFieldBuilder.product)

		PostVerificationFieldBuilder.requisites={'key':'about','required':True}
		PostVerificationFieldBuilder.add(String('(?=.*(?:[a-zA-Z].*){5}).+'))
		PostVerificationTemplateBuilder.add(PostVerificationFieldBuilder.product)

	else:
		PostVerificationFieldBuilder.requisites={'key':'identification','required':True}
		PostVerificationFieldBuilder.add(String('^((?:\w{6,30})|(?:(?=[\w_\-\.]+\@\w+\.\w+)[\w_\-\.@]{5,60}))$'))
		PostVerificationTemplateBuilder.add(PostVerificationFieldBuilder.product)

	return PostVerificationTemplateBuilder.product


