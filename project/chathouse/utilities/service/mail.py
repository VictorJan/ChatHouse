from flask_mail import Mail,Message

mail=Mail()

class MailService:
	@staticmethod
	def send(**payload):
		'''
		Goal: send an email message to a certain email, with data passed in the payload.
		Payload must contain data and recipient keys.
		'''
		items=('recipients','body','subject')
		if len(parsed:=dict(filter(lambda item:item[0] in items,payload.items())))==len(items):
			mail.send(Message(**parsed))
			return None
		raise Exception('Invalid payload')