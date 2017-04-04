import datetime
import uuid
import dimensions
import urllib

from peewee import *
from models import DATABASE


class BaseModel(Model):
	class Meta:
		database = DATABASE


class Deals(BaseModel):
	productId = PrimaryKeyField()
	productName = CharField()
	productImageURI = CharField()
	productDealText = CharField()
	productDealDate = DateField()


def create(**kwargs):
	Deals.create(**kwargs)


def get():
	deals = Deals.select().order_by(fn.Rand()).limit(1).execute()
	for deal in deals:
		temp_file = urllib.urlretrieve(deal.productImageURI)
		dims = dimensions.dimensions(temp_file[0])
		response = {
			"style": "media",
			"id": str(uuid.uuid4()),
			"url": "https://jmart.com/shop/product.f90?productID=" + deal.productName,
			"title": deal.productName,
			"description": {
				"value": deal.productDealText,
				"format": "text",
			},
			"thumbnail": {
				"url": deal.productImageURI,
				"url@2x": deal.productImageURI,
				"width": dims[0],
				"height": dims[1]
			}
		}
	return response
