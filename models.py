import datetime

from peewee import *


DATABASE = MySQLDatabase('hn5', host="localhost", user="root", passwd="littleredunicorns")


class BaseModel(Model):
	class Meta:
		database = DATABASE


class Rollbacks(BaseModel):
	rollback_id = PrimaryKeyField()
	rollback_story_number = IntegerField(index=True)
	rollback_story_name = CharField()
	rollback_blame = CharField(index=True)
	date_created = DateTimeField(default=datetime.datetime.now())


class BS(BaseModel):
	bs_id = PrimaryKeyField()
	bs_phrase = CharField()
	bs_index = CharField(index=True)
	bs_creator = CharField(index=True)
	date_created = DateTimeField(default=datetime.datetime.now())


class Subscribers(BaseModel):
	subscriber_id = PrimaryKeyField()
	subscriber_name = CharField(null=True)
	subscriber_email = CharField(null=True)
	subscriber_number = CharField(index=True, unique=True)


class Messages(BaseModel):
	message_id = PrimaryKeyField()
	message_text = CharField(max_length=918)
	message_type = IntegerField()
	message_created = DateTimeField(default=datetime.datetime.now())


class Questions(BaseModel):
	question_id = PrimaryKeyField()
	question_text = TextField()
	question_sender = CharField()
	question_sender_name = CharField(default=None)
