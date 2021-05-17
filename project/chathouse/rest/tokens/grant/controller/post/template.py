from chathouse.utilities.security.validation.data.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field import Field


def create_a_template(route):

	'''
	Goal: create a template for validating data , depending on th initial route,  in the post requests aimed at the /api/tokens/grant.

	Actions:
		Using the TemplateBuilder class - create an instance of PostGrantTemplateBuilder.
		Add a neccessary field "password" with proper requirements : a string of 64 characters - the sha256 hexdigested hash.
		If the route is signup:
			Add a neccessary field "keyring" , with requirements : data type must be a dictionary, it shall contain:
				public_key : value of which must be a string;
				g: value of which must be an int;
				m: value of which must also be an int;
				private_key : value of which must be a dictionary containing:
					iv: value of which must be a string;
					data: value of which must be a string as well.

			Return the instance of the Template class from the builder, thus reseting the PostGrantTemplateBuilder.

	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - template.
	
	Exceptions:
		Raises:
			ValueError - if the provided route argument doesn't fall under any of the alternative values.
	'''
	
	assert any(map(lambda a: route==a,('signup','login'))), ValueError('The route argument shall have a value of "signup" or "login".')

	PostGrantTemplateBuilder=TemplateBuilder()
	PostGrantTemplateBuilder.add(Field('password',regex='^\w{64}$',data_type=str))
	
	if  route=='signup':
		
		required_keys_n_types={
			'public_key':int,
			'private_key':{
				'iv':str,
				'data':str
			},
			'g':int,
			'm':int
		}

		PostGrantTemplateBuilder.add(Field('keyring',keys=required_keys_n_types,data_type=dict))

	return PostGrantTemplateBuilder.template