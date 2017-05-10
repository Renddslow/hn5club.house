from flask import Blueprint, jsonify

from services.trump.trump import TrumpNews

trump_api = Blueprint("services.trump.service", __name__)


@trump_api.route("/api/v1/trump", methods=['GET', 'POST'])
def trump():
	trump = TrumpNews()
	news = trump.get_trump_news()
	response = {
		"message": news['url'],
		"color": "yellow",
		"notify": False,
		"card": news
	}
	return jsonify(response)
