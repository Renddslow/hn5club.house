from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom
from dateutil import tz
import datetime
import uuid
import json
import random

import requests
from flask import Flask, jsonify, request, render_template, Response, g
import redis

from lonely import Lonely
from models import DATABASE

from services.tweet.service import tweet_api
from services.bs.service import bs_api
from services.trump.service import trump_api
from services.word.service import word_api
from services.magic8.service import magic8_api
from services.tankslayer.service import tankslayer_api
from services.dungeon.service import dungeon_api

application = Flask(__name__)

application.register_blueprint(tweet_api)
application.register_blueprint(bs_api)
application.register_blueprint(trump_api)
application.register_blueprint(word_api)
application.register_blueprint(magic8_api)
application.register_blueprint(tankslayer_api)
application.register_blueprint(dungeon_api)

@application.before_request
def before_request():
	g.db = DATABASE
	g.db.connect()
	g.r = redis.StrictRedis(host='localhost', port=6379, db=2)

@application.after_request
def after_request(response):
	g.db.close()
	return response

@application.route("/")
def home():
	title = "HN5 Clubhouse"
	footer = "Check out the <a href='/legacy'>wall of legacy</a>"
	return render_template("countdown.html", title=title, footer=footer)


@application.route("/legacy")
def legacy():
	title = "The Wall of Legacy | HN5 Clubhouse"
	people = requests.get("http://hn5club.house/api/v1/legacy").json()['people']
	footer = "<a href='/'>Countdown</a> to the immeninent demise of HN5"
	return render_template("legacy.html", title=title, footer=footer, people=people)


@application.route("/api/v1/daysLeft")
def daysLeft():
	from_zone = tz.gettz("UTC")
	to_zone = tz.gettz("America/Chicago")
	
	then_utc = datetime.datetime(2017,7,6,16,0,0)
	then_utc = then_utc.replace(tzinfo=from_zone)
	
	now_utc = datetime.datetime.now()
	now_utc = now_utc.replace(tzinfo=from_zone)

	then_cdt = then_utc.astimezone(to_zone)
	now_cdt = now_utc.astimezone(to_zone)
	
	delta = then_cdt - now_cdt
	
	if delta.days < 0:
		message = "HN5 No Longer Exists"
	else:
		message = delta.days

	return jsonify({"daysLeft": message})


@application.route("/api/v1/legacy", methods=['GET','POST'])
def legacy_api():
	if request.method == "GET":
		people = g.r.lrange("hn5:people:legacy", 0, -1)
		return jsonify({"people": people})
	else:
		form = request.form
		for name in form['names'].split(","):
			g.r.rpush("hn5:people:legacy", name.strip())

		return jsonify({"message": "They have been added to the wall of legacy. They will be missed."})


@application.route("/api/v1/inspire", methods=['GET','POST'])
def inspire():
	image = requests.get("http://inspirobot.me/api?generate=true").text
	message = {
		"style": "image",
		"id": str(uuid.uuid4()),
		"url": image,
		"title": "Be inspired",
		"thumbnail": {
			"url": image,
			"url@2x": image,
			"width": 650,
			"height": 650
		}
	}
	card = {
		"color": "red",
		"message": image,
		"message_format": "text",
		"notify": True
	}
	return jsonify(card)


@application.route("/api/v1/lonely/subscribe", methods=['GET', 'POST'])
def subscribe():
	lonely = Lonely()
	if request.form['Body'].lower().find("unsubscribe") > -1:
		message = "Sorry to see you go! If you would like to resubscribe simply reply with SUBSCRIBE."
	elif request.form['Body'].lower().find("subscribe") > -1:
		message = lonely.subscribe(request.form['From'])
	else:
		message = "Welcome to Lonely Places, if you would like to subscribe reply with SUBSCRIBE. If you're already subscribed and want to unsubscribe, reply with UNSUBSCRIBE."
	response = Element('Response')
	message_tag = SubElement(response, 'Message')
	message_tag.text = message
	return Response(prettify(response), mimetype='text/xml')


@application.route("/api/v1/lonely/messages", methods=['GET'])
def lonely_messages():
	lonely = Lonely()
	day_of_week = datetime.datetime.today().weekday() + 1
	if day_of_week == 1:
		day_of_week = 8
	message = lonely.get_messages(day_of_week)
	lonely.get_subscribers(message)
	return jsonify(True)


@application.route("/api/v1/lonely/messages", methods=['POST'])
def create_lonely_message():
	lonely = Lonely()
	data = {
		"message_type": request.form['message_type'],
		"message_text": request.form['message_text'],
		"message_created": request.form['message_created']
	}
	new_message = lonely.create_message(data)
	if new_message:
		return jsonify({"message": "success"})
	else:
		return jsonify({"message": "failure"})


def prettify(elem):
	rough_string = ElementTree.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent="  ")


if __name__ == "__main__":
	application.run(host="0.0.0.0")
