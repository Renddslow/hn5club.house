import requests
import uuid
import dimensions
import urllib
import random


class TrumpNews:
	def __init__(self):
		self.key = "0b51b400918d4c098a37faa733337e9f"
		self.sources = ["buzzfeed", "bbc-news", "the-new-york-times", "bloomberg", "cnn",
						"the-wall-street-journal", "associated-press", "associated-press",
						"google-news", "newsweek", "the-huffington-post",
						"the-washington-post", "time", "usa-today", "wired"]
		random.shuffle(self.sources)
		self.url_base = "https://newsapi.org/v1/articles"
		self.params = {
			"source": "",
			"sortBy": "top",
			"apiKey": self.key
		}


	def get_news_source(self, source):
		self.params["source"] = source
		news = requests.get(url=self.url_base, params=self.params)
		return news.json()

	
	def check_for_trump(self, news):
		for article in news['articles']:
			if article['description'].find("Trump") > -1 or article['title'].find("Trump") > -1:
				return article


	def get_trump_news(self):
		for source in self.sources:
			news = self.get_news_source(source)
			trumped = self.check_for_trump(news)
			if trumped:
				return self.render_news(trumped)
	
	
	def render_news(self, trump):
		temp_file = urllib.urlretrieve(trump["urlToImage"])
		dims = dimensions.dimensions(temp_file[0])
		response = {
			"style": "media",
			"id": str(uuid.uuid4()),
			"url": trump["url"],
			"title": trump["title"],
			"description": {
				"value": trump["description"],
				"format": "text"
			},
			"thumbnail": {
				"url": trump["urlToImage"],
				"url@2x": trump["urlToImage"],
				"width": dims[0],
				"height": dims[1]
			}
		}
		return response
