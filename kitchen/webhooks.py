from api.serializers import JudgementSerializer
import requests
import json
from rest_framework.renderers import JSONRenderer

def webhook(dataset, url):
	print dataset
	print url
	if url:
		try:
			headers = {'Content-type': 'application/json'}
			# send a request with json data and timeout of 2 seconds
			r = requests.post(url, data = json.dumps(dataset), headers = headers)
			return r
		except:
			print 'webhook was not successful'
			return False
	return False

def webhook_results(judgements, url):
	if url:
		dataset = []

		for judgement in judgements:
			
			
			dataset.append(JudgementSerializer(judgement).data)
			#dataset.append(JSONRenderer().render(judgement_serializer.data))
		
		print webhook(dataset, url)
	return False
def webhook_quality_conrol(judgement, url):
	if url and judgement.unit.judgements.filter(gold = True).count()>0:
		dataset = []
		
		dataset.append(JudgementSerializer(judgement).data)
		dataset.append(JudgementSerializer(judgement.unit.judgements.filter(gold = True).all()[0]).data)
		
		evaluation = webhook(dataset, url)
		
		if evaluation:
			if evaluation.status_code in [201,200]:
				judgement.score = 1
			if evaluation.status_code in [500]:
				judgement.score = -1
			judgement.save()
	return False