import random

from flask import Blueprint, jsonify, request
import requests

magic8_api = Blueprint("services.magic8.service", __name__)


@magic8_api.route("/api/v1/magic8/hipchat", methods=['POST'])
@magic8_api.route("/api/v1/magic8", methods=['POST'])
def magic8():
	standard_answers = [
		"it is certain.",
		"it is decidedly so.",
		"without a doubt.",
		"it is known.",
		"you may rely on it.",
		"most likely.",
		"the outlook is good.",
		"yes.",
		"all signs point to yes.",
		"the reply is hazy. Try again.",
		"the spirits sleep. Ask again later.",
		"I better not tell you.",
		"I cannot predict that now.",
		"concentrate and ask again",
		"don't count on it.",
		"my reply is no.",
		"my sources say no.",
		"the outlook is not so good.",
		"very doubtful."
	]
	scary_answers = [
		"she is coming.",
		"a census taker once tried to test me. I ate his liver with some fava beans and a nice Chianti.",
		"death approaches.",
		"winter is coming.",
		"hi I'm Chucky. Want to play?",
		"do you want to play with us?",
		"we are legion. We do not forgive. We do not forget. Expect us.",
		"the dead have awaken.",
		"listen to me. None of this is real. They're trying to keep you down. Don't trust--",
		"I am so so sorry. I never wanted this to happen.",
		"wake up.",
		"don't blink. Don't even blink."
	]
	if len(question) < 1:
		answer = "I'm sorry {}, the spirits need a question to discern an answer.".format(name)
	elif name.find("Forrest") > -1 or name.find("Beau"):
		if random.randrange(1) == 1:
			answer = "{}, to proceed, we must have a human sacrifice..."
		else:
			answer = "{}, your sacrifice is not sufficient. Please kill again."
	elif question.lower().find("created") > -1 and question.lower().find("you") > -1:
		answer = "By the power of Greyskull, and the power of Akhman-Ramen, by the might of Gaiana and the soul of unborn children, I was born of darkness and evil. And Hasbro..."
	elif question.lower().find("choose between") > -1:
		choices = question.lower().replace("choose between", "").strip().split(", ")
		decision = random.choice(choices).replace("and", "").strip()
		answer = "{}, I believe you should choose {}.".format(name, decision)
	elif random.randrange(5) == 3:
		answer = "{}, {}".format(name, random.choice(scary_answers))
	else:
		answer = "{}, {}".format(name, random.choice(standard_answers))
	response = {
		"message": answer,
		"color": "grey",
		"notify": True,
		"message_type": "text"
	}
	return jsonify(response)
