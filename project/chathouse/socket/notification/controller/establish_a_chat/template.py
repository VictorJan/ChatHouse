from chathouse.utilities.security.validation.data.builder import TemplateBuilder
from chathouse.utilities.security.validation.data.field import Field


def create_a_template():

	'''
	Goal: create a template for validating data , depending on the initial event, aimed at the /notification [establish_a_chat].

	Actions:
		Using the TemplateBuilder class - create an instance of Establish_a_ChatTemplateBuilder.
		Add a neccessary field "name" with proper requirements : a string of at least 4 characters/spaces long , 30 characters/spaces max and with at least 4 characters in it. 
		Add a non required field "participant_id" : value of which must be an integer;
		[!Note!] - the latter field - "participant_id" is set up as non required, due to the permitions to start chats without any participants.
		Return the instance of the Template class from the builder, thus reseting the Establish_a_ChatTemplateBuilder.

	Returns: instance of the Template class from the builder, using a property of the TemplateBuilder - template.
	'''
	
	Establish_a_ChatTemplateBuilder=TemplateBuilder()
	Establish_a_ChatTemplateBuilder.add(Field('name',regex='^(?=.*(?:\w.*){4,})[\w\s]{4,30}$',data_type=str))
	Establish_a_ChatTemplateBuilder.add(Field('participant_id',required=False,data_type=int))

	return Establish_a_ChatTemplateBuilder.template