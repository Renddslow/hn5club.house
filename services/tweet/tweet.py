import tweepy

CONSUMER_KEY = "isVH6mi3jPE7HNLSFUYAnE57I"
CONSUMER_SECRET = "RPoM0AjSvFw8GPGq0m5sKJCg8s3ElRONYKl9qeRJmQcH1CVk1u"
ACCESS_TOKEN = "804421794237063168-r3U25yBIrFhCjUdYZrQq2QSzHiIWOxj"
ACCESS_TOKEN_SECRET = "ZVyxQaHORTwmCrm21Evj9WRqXKiEGZ7lDZENfa6qpGfns"

def post_tweet(message):
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)
	api.update_status(message)
	return True
