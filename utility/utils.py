import requests 

from kitchen.models import Job, Unit
from rewards.models import Coupon
from models import Attachment

import re
import csv
import urllib2
import StringIO
import scraperwiki

def saveUnits(job, dataset):
	units = []
	if len(dataset)>0:
		for item in dataset:
			dataitem = Unit(job = job, input_data = item)
			dataitem.save()

			units.append(dataitem.id)
	return units
def collectDataFromCSV(url):
	dataset = []
	
	pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	data = scraperwiki.scrape(url)
	reader = csv.reader(data.splitlines(), delimiter = ';')
	
	i = 0
	for row in reader:    
		if i == 0:
			headers = row
		else:
			dataitem = {}
			for j in range(len(row)):
				dataitem[headers[j]] = pattern.sub(u'\uFFFD', row[j]).decode('latin-1').encode("utf-8")
			dataset.append(dataitem)
		i+=1
	return dataset

