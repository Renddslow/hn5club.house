import uuid

from flask import Blueprint, jsonify, request
import requests
from pyquery import PyQuery as pq
from BeautifulSoup import BeautifulSoup

word_api = Blueprint("services.word.service", __name__)


@word_api.route("/api/v1/word", methods=['GET', 'POST'])
def urban_dict_get():
	if request.method == "POST":
		message = request.get_json()['item']['message']['message'].replace("/ud", "").strip()
	else:
		message = request.args.get("term")
	if message and len(message):
		ud = requests.get("http://www.urbandictionary.com/define.php?term={}".format(message))
	else:
		ud = requests.get("http://www.urbandictionary.com/random.php")
	d = pq(ud.text)
	title = d(".word:first").html()
	meaning = BeautifulSoup(d(".meaning:first").html().replace("\n", "")).text
	card = {
		"style"	: "media",
		"id": str(uuid.uuid4()),
		"url": ud.url,
		"title": title,
		"description": {
			"value": meaning,
			"format": "text"
		},
		"thumbnail": {
			"url": "https://images.unsplash.com/photo-1490682143684-14369e18dce8?dpr=1&auto=format&fit=crop&w=500&h=300&q=80&cs=tinysrgb&crop=",
			"url@2x": "https://images.unsplash.com/photo-1490682143684-14369e18dce8?dpr=1&auto=format&fit=crop&w=1000&h=667&q=80&cs=tinysrgb&crop=",
			"width": 500,
			"height": 300
		}
	}
	response = {
		"color": "yellow",
		"message": "ud",
		"notify": True,
		"card": card
	}
	return jsonify(response)


@word_api.route("/api/v1/seo/meta", methods=['POST'])
def seo_meta():
	urls = request.form['urls']
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
	response = []
	for url in urls.split(","):
		seo = requests.get(url, verify=False, headers=headers)
		d = pq(seo.text)
		data = {
			"url": url,
			"title": d("title").html(),
			"description": d("meta[name='description']").attr("content"),
			"canonical": d("link[rel='canonical']").attr("href")
		}
		response.append(data)
	return jsonify(response)
