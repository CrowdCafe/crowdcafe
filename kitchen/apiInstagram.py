# -*- coding: utf-8 -*- 
import json
import pprint
import urllib2
from django.conf import settings

#---------------------------------------------------------------------------
# A class for collecting data from Instagram
class InstagramCall:
	def __init__(self, client_id, client_secret):
		self.client_id = client_id
		self.client_secret = client_secret
		self.api_url = 'https://api.instagram.com/'
		self.api_version = 'v1/'

	def retreiveData(self,url):
		
		
		response = urllib2.urlopen(url)
		#print response.read()
		json_response = json.loads(response.read())
		return json_response

	def getByKeyword(self,tag_name, count ,max_id=False):
		call = '/tags/'+str(tag_name)+'/media/recent?count='+str(count)
		if max_id:
			call+='&MAX_ID='+str(max_id)
		url = self.api_url+self.api_version+call+'&client_id='+self.client_id
		data = []
		while len(data) < count:
			print url
			print len(data)
			resp = self.retreiveData(url)
			data = data + resp['data']
			url = resp['pagination']['next_url']

		return data