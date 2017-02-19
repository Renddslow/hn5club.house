from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom
import datetime

from flask import Flask, jsonify, request, render_template, Response

from tweet import post_tweet
from rollback import get_time_since_rollback, parse_message
from corporate import Corporate
from trump import TrumpNews
from lonely import Lonely 


application = Flask(__name__)


@application.route("/")
def home():
	return "<h1 style='text-align: center; width: 100%;'>Welcome to HN5 Clubhouse. Where the karma is cheap and the laughs are hearty.</h1>"


@application.route("/api/v1/tweet", methods=['POST'])
def tweet():
	request_from_hipchat = request.get_json()
	message = request_from_hipchat['item']['message']['message'].replace("/tweet ", "")
	from_person = request_from_hipchat['item']['message']['from']['name']
	post_was_successful = post_tweet(message)
	response = {}

	if post_was_successful:
		response = {
			"message": "It worked! {} said {}".format(from_person, message),
			"color": "purple",
			"notify": "true",
			"message_format": "text"
		}
	
	return jsonify(response)


@application.route("/api/v1/playlist/add", methods=['POST'])
def add_to_playlist():
	request_from_hipchat = request.get_json()
	message = request_from_hipchat['item']['message']['message'].replace("/playlist ", "")
	from_person = request_from_hipchat['item']['message']['from']['name']
	response = {
		"message": "Good choice, {}. Adding {} to the HN5 Playlist!".format(from_person, message),
		"color": "green",
		"notify": "true",
		"message_format": "text"
	}
	return jsonify(response)



@application.route("/api/v1/rollback", methods=['POST'])
@application.route("/api/v1/rollback/hipchat", methods=['POST'])
def rollback():
	if 'hipchat' in request.url_rule.rule:
		request_from_hipchat = request.get_json()
		message = request_from_hipchat['item']['message']['message']
	else:
		message = request.form['message']
	print(message)
	action = "get" if len(message.strip()) == 9 else "post"
	if action == "get":
		response = get_time_since_rollback()
	if action == "post":
		response = parse_message(message)
	return jsonify(response)


@application.route("/api/v1/bs", methods=['GET'])
@application.route("/api/v1/bs/hipchat", methods=['POST'])
def bs():
	request_from_hipchat = request.get_json()
	if 'hipchat' in request.url_rule.rule:
		username = request_from_hipchat['item']['message']['from']['mention_name']
	else:
		username = "WebUser"
	corp = Corporate(username)
	response = {
		"message": corp.create_corporate_bs(),
		"color": "yellow",
		"notify": True,
		"message_format": "text"
	}
	return jsonify(response)



@application.route("/api/v1/trump", methods=['GET', 'POST'])
def trump():
	trump = TrumpNews()
	news = trump.get_trump_news()
	response = {
		"color": "yellow",
		"message": news["url"],
		"notify": False,
		"card": news
	}
	return jsonify(response)


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


def prettify(elem):
	rough_string = ElementTree.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent="  ")


if __name__ == "__main__":
	application.run(host="0.0.0.0")
