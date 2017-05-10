from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom
import datetime
import uuid
import json
import random

from flask import Flask, jsonify, request, render_template, Response, g

from lonely import Lonely
from models import DATABASE

from services.tweet.service import tweet_api
from services.bs.service import bs_api
from services.trump.service import trump_api
from services.word.service import word_api
from services.magic8.service import magic8_api
from services.tankslayer.service import tankslayer_api

application = Flask(__name__)

application.register_blueprint(tweet_api)
application.register_blueprint(bs_api)
application.register_blueprint(trump_api)
application.register_blueprint(word_api)
application.register_blueprint(magic8_api)
application.register_blueprint(tankslayer_api)

@application.before_request
def before_request():
	g.db = DATABASE
	g.db.connect()

@application.after_request
def after_request(response):
	g.db.close()
	return response

@application.route("/")
def home():
	return "<h1 style='text-align: center; width: 100%;'>Welcome to HN5 Clubhouse. Where the karma is cheap and the laughs are hearty.</h1>"


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
