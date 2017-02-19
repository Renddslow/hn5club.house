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