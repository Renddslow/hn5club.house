from datetime import datetime

from twilio.rest import TwilioRestClient
import models


class Lonely:
	def __init__(self):
		account_sid = "ACc56b20987803dcf1a9e9f8131356b465"
		auth_token = "0d4671ce138ff7d3d0ede5002c3cc43d"
		self.client = TwilioRestClient(account_sid, auth_token)
		self.number = "+14026717306"

	
	def subscribe(self, recipient):
		try:
			subscriber = models.Subscribers.get(subscriber_number = recipient)
		except models.Subscribers.DoesNotExist:
			models.Subscribers.create(
				subscriber_number = recipient
			)
			message = models.Messages.get(message_id = 1).message_text
		else:
			message = "Oops, looks like you're already subscribed."
		return message

	
	def unsubscribe(self, recipient):
		try:
			subscriber = models.Subscribers.get(subscriber_number = recipient)
		except models.Subscribers.DoesNotExist:
			message = "Oops, it doesn't look like you've subscribed yet."
		else:
			subscriber.delete_instance()
			message = "We're sorry to see you go. Remember you can easily SUBSCRIBE any time you want."
		return message
			
	
	def get_messages(self, type_):
		message = models.Messages.select()\
						.where(models.Messages.message_type == type_,
							models.Messages.message_created < datetime.now())\
						.order_by(models.Messages.message_created.desc())\
						.get()
		return message.message_text


	def create_message(self, data):
		try:
			models.Messages.create(**data)
		except:
			return False
		else:
			return True
		

	def get_subscribers(self, message):
		subscribers = models.Subscribers.select()
		subscriber_list = []
		for subscriber in subscribers.execute():
			self.send_message(subscriber.subscriber_number, message)

	
	def send_message(self, recipient, message):
		message = self.client.messages.create(
			body=message,
			to=recipient, 
			from_=self.number
		)
