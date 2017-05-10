from flask import Blueprint, jsonify, request
import requests

yarr_api = Blueprint("services.yarr.service", __name__)


@yarr_api.route("/api/v1/yarr/hipchat", methods=['POST'])
@yarr_api.route("/api/v1/yarr", methods=['POST'])
def pirate_speak():
	if "hipchat" in request.url_rule.rule:
		message = request.get_json()['item']['message']['message'].replace("/yarr", "").strip()
	else:
		message = request.get_json()['text']
	headers = { "X-Funtranslations-Api-Secret": "W_yk6LDtNye2t_mHKhBJqQeF" }
	pirate_url = "http://api.funtranslations.com/translate/pirate.json"
	try:
		_request = requests.post(url=pirate_url, headers=headers, data={"text": message}).json()
		pirate_speak = _request["contents"]["translated"]
	except Exception as e:
		pirate_speak = "Yarr it looks like there be a problem hookin' up our ship to the cap'n ship. Ye may have been fiddlin wit her too much."
		pirate_speak += "Here be what the cap'n say: {}".format(_request["error"]["message"])
	pirate_speak = pirate_speak.lower().replace("that's what she said", "aye that be what the wench said to ye priest")
	pirate_speak = pirate_speak.replace("netstudio", "that pile of bilge")
	pirate_speak = pirate_speak.replace("vba", "a poor man's stench")
	pirate_speak = pirate_speak.replace("php", "pig's bottom")
	pirate_speak = pirate_speak.replace("coldfusion", "me ex-lover's cold heart")
	pirate_speak = pirate_speak.replace(" is ", " be ")
	response = {
		"color": "red",
		"message": pirate_speak,
		"notify": True,
		"message_type": "text"
	}
	return jsonify(response)
