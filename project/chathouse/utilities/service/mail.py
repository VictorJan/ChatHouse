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
		if all(map(lambda key: key in payload,items)):
			try:
				mail.send(Message(**payload))
			finally:
				return None
		raise Exception('Invalid payload')