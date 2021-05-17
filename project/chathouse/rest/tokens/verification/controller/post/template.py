from chathouse.utilities.security.validation.data.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field import Field


def create_a_template(route):

	'''
	Goal: create a template based on the initial route of the requrest.
	Arguments: route:str , expecting alternatives = signup/login.
	Actions:
		Using the TemplateBuilder class - create an instance of PostVerificationTemplateBuilder.
		If the route is signup:
			Add neccessary fields with proper requirements : email,username,name and about.
			Return the instance of the Template class from the builder, thus reseting the PostVerificationTemplateBuilder.
		Otherwise:
			Add a neccessary field with proper requirements - identification.
			Return the instance of the Template class from the builder.
	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - template.
	
	Exceptions:
		Raises:
			ValueError - if the provided route argument doesn't fall under any of the alternative values.
	'''
	
	assert any(map(lambda a: route==a,('signup','login'))), ValueError('The route argument shall have a value of "signup" or "login".')

	PostVerificationTemplateBuilder=TemplateBuilder()
	if  route=='signup':
		PostVerificationTemplateBuilder.add(Field('email',regex='^(?=[\w_\-\.]+\@\w+\.\w+)[\w_\-\.@]{5,60}$',data_type=str)) #^(?=[\w_\-\.]+\@\w+\.\w+)[\w_\-\.@]{5,40}$
		PostVerificationTemplateBuilder.add(Field('username',regex='^\w{6,30}$',data_type=str))
		PostVerificationTemplateBuilder.add(Field('name',regex='[a-zA-Z]{3,25}',data_type=str))
		PostVerificationTemplateBuilder.add(Field('about',data_type=str))

		return PostVerificationTemplateBuilder.template

	PostVerificationTemplateBuilder.add(Field('identification',regex='^((?:\w{6,30})|(?:(?=[\w_\-\.]+\@\w+\.\w+)[\w_\-\.@]{5,40}))$',data_type=str))

	return PostVerificationTemplateBuilder.template


