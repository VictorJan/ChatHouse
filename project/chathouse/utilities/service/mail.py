from flask_mail import Mail,Message
from chathouse.utilities.service.asynchronous import asynchronous

mail=Mail()

class MailService:
	
	@staticmethod
	@asynchronous
	def send(**payload):
		'''
		Goal: executite an asynchronous dispatch of an email to a certain email address, based on the data provided in the payload.
		Arguments: payload - key-word-argument. Expecting: recipients:list|tuple , body:str , subject:str , app:app instance.
		Actions:
			Having set the app instance - proceed to send an email , using the Message instance in the app context.
		Excpetions:
			Raises:
				ValueError - if the payload doesn't follow the established guidelines for the arguments.
				ValueError - if the app key word argument is not provided or the class of the instance is invalid.
			If any exceptions related to the app_context shall arise - then ignore them.
		'''

		items = ( ('recipients',(list,tuple)) , ('body',str) , ('subject',str))

		assert all(map(lambda item: (value:=payload.get(item[0]),None) is not None and isinstance(value,item[1]) ,items)) , ValueError('Invalid payload. The payload shall contain key with respected data types as such - recipients:list|tuple , body:str , subject:str.')
		assert (app:=payload.pop('app',None)) is not None and hasattr(app,'app_context'), ValueError('The "app" agrument shall be present and contain a context attribute.')

		try:
			with app.app_context():
				mail.send(Message(**payload))
		except:
			pass

		return None