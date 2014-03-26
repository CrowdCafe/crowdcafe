# -*- coding: utf-8 -*- 
from twython import Twython
from django.shortcuts import get_object_or_404
from django.conf import settings
from social_auth.models import UserSocialAuth
from django.contrib.auth.models import User


class TwitterCall(object):
	TWITTER_APP_KEY = settings.TWITTER_CONSUMER_KEY
	TWITTER_APP_KEY_SECRET = settings.TWITTER_CONSUMER_SECRET
	
	def __init__(self, client_id=None, client_secret=None):
		self.client_id = client_id
		self.client_secret = client_secret
		self.call = Twython(app_key=self.TWITTER_APP_KEY, 
			app_secret=self.TWITTER_APP_KEY_SECRET, 
			oauth_token=client_id, 
			oauth_token_secret=client_secret)

	def getByKeyword(self,hashtag,count=20, max_id = False):
		print self.call
		print hashtag
		#hashtag=hashtag
		search = self.call.search(q=hashtag, count=count)
		tweets = search['statuses']
		return tweets
