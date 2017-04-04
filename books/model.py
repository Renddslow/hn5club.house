from peewee import *


DATABASE = MySQLDatabase("books", host="localhost", user="root", passwd="littleredunicorns")


class BaseModel(Model):
	class Meta:
		database = DATABASE


class Authors(BaseModel):
	
