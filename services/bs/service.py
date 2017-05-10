from flask import Blueprint, jsonify, request

from services.bs.corporate import Corporate

bs_api = Blueprint("services.bs.service", __name__)


@bs_api.route("/api/v1/bs", methods=['GET'])
@bs_api.route("/api/v1/bs/hipchat", methods=['POST'])
def bs():
	if 'hipchat' in request.url_rule.rule:
		request_from_hipchat = request.get_json()
		username = request_from_hipchat['item']['message']['from']['mention_name']
	else:
		username = "WebUser"
	corp = Corporate(username)
	response = {
		"message": corp.create_corporate_bs(),
		"color": "yellow",
		"notify": True,
		"message_type": "text"
	}
	return jsonify(response)
