from flask import Blueprint, jsonify, request
import requests

tankslayer_api = Blueprint("services.tankslayer.service", __name__)


@tankslayer_api.route("/api/v1/tankSlayer", methods=['GET', 'POST'])
def tankSlayer():
	params = {
		"firstName": "Tank",
		"lastName": "Slayer"
	}
	tankSlayer = requests.get(url="http://api.icndb.com/jokes/random", params=params)
	message = tankSlayer.json()['value']['joke']
	if request.method == 'POST':
		response = {
			"message": message,
			"color": "red",
			"notify": False,
			"message_type": "text"
		}
	else:
		response = { "message": message }
	return jsonify(response)
