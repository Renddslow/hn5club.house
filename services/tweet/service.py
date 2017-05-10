from flask import Blueprint, jsonify

from tweet import post_tweet

tweet_api = Blueprint("services.tweet.service", __name__)


@tweet_api.route("/api/v1/tweet", methods=['POST'])
	request_from_hipchat = request.get_json()
	message = request_from_hipchat['item']['message']['message'].replace("/tweet ", "")
	from_person = request_from_hipchat['item']['message']['from']['name']
	post_was_successful = post_tweet(message)
	response = {
		"color": "purple",
		"notify": "true",
		"message_format": "text"
	}
	if post_was_successful:
		response['message'] = "It worked! {} said {}".format(from_person, message)
	else:
		response['message'] = "There was a problem, {}"\
								.format(from_person.split(" ")[0])
	return jsonify(response)
