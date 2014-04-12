# -*- coding: utf-8 -*- 
import json
import pprint
import urllib2
from django.conf import settings

#---------------------------------------------------------------------------
# A class for collecting data from Instagram
class InstagramCall:
	def __init__(self):
		self.client_id = settings.INSTAGRAM_CLIENT_ID
		self.client_secret = settings.INSTAGRAM_SECRET
		self.api_url = 'https://api.instagram.com/'
		self.api_version = 'v1/'

	def retreiveData(self,call):
		url = self.api_url+self.api_version+call+'&client_id='+self.client_id
		response = urllib2.urlopen(url)
		#print response.read()
		json_response = json.loads(response.read())
		return json_response['data']

	def getByKeyword(self,tag_name='ufacity',count=20,max_id=False):
		call = '/tags/'+str(tag_name)+'/media/recent?count='+str(count)
		if max_id:
			call+='&MAX_ID='+str(max_id)
		print call
		return self.retreiveData(call)