from api.serializers import JudgementSerializer
import requests
import json
from rest_framework.renderers import JSONRenderer
import logging
from kitchen.models import Judgement

log = logging.getLogger(__name__)

def createJudgement(unit, postdata, worker, gold_creation):
	judgement_output_data = {}
	score = 0.0
	for key in postdata:
		# only if a POST data has a key with dataunit_handle - it will be saved (otherwise we can not find a connection to a specific unit)
		dataunit_handle = 'dataitem_'+str(unit.id)
		if dataunit_handle in key:
			judgement_output_data[key.replace(dataunit_handle,'')] = postdata[key]
			# check gold data if gold exists but qualitycontrol_url is not given
			if unit.gold:
				gold_judgement_data = unit.judgements.filter(gold = True).all()[0].output_data
				if not unit.job.qualitycontrol.qualitycontrol_url and 'gold'+key.replace(dataitem_handle,'') in gold_judgement_data:
					#TODO rethink it
					if postdata[key] == gold_judgement_data['gold'+key.replace(dataitem_handle,'')]:
						score+=1.0
					else:
						score-=1.0
	judgement = Judgement(unit = unit, output_data =judgement_output_data, worker = worker, score = score)
	# if it was a gold creation task and the worker is a member of the job app account
	if gold_creation and worker in unit.job.app.account.users.all():
		judgement.gold = True
	# notice that we don't save the judgement - it will be saved in webhook_quality_conrol
	return judgement

def saveJudgements(units, postdata, worker, gold_creation):
	judgements = []
	for unit in units:
		judgement = createJudgement(unit, postdata, worker, gold_creation)
		log.debug('new judgement: '+str(judgement))
		judgement = webhook_quality_conrol(judgement,judgement.unit.job.qualitycontrol.qualitycontrol_url)
		judgements.append(judgement)
	# send a request to URL defined in job settings with info about judgements provided
	webhook_results(judgements, units[0].job.judgements_webhook_url)
	    
def webhook(dataset, url):
	log.debug('send webhook request with data: '+str(dataset)) 
	log.debug('send webhook request to url: '+str(url)) 
	if url:
		try:
			headers = {'Content-type': 'application/json'}
			# send a request with json data and timeout of 2 seconds
			r = requests.post(url, data = json.dumps(dataset), headers = headers)
			log.debug('webhook: '+str(r)) 
			return r
		except:
			log.debug('webhook was not successful') 
			return False
	return False

def webhook_results(judgements, url):
	if url:
		dataset = []

		for judgement in judgements:
			dataset.append(JudgementSerializer(judgement).data)
		return webhook(dataset, url)
	return False

def webhook_quality_conrol(judgement, url):
	log.debug('start quality control '+str(judgement)+' url: '+str(url)) 
	if url and judgement.unit.gold:
		dataset = []
		
		dataset.append(JudgementSerializer(judgement).data)
		dataset.append(JudgementSerializer(judgement.unit.judgements.filter(gold = True).all()[0]).data)
		
		log.debug('dataset: '+str(dataset)) 
		
		evaluation = webhook(dataset, url)
		
		log.debug('evaluation: '+str(evaluation)) 
		if evaluation:
			log.debug('evaluation status code: '+str(evaluation.status_code)) 
			if evaluation.status_code in [201,200]:
				d = evaluation.json()
				log.debug('evaluation data: '+str(d)) 
				if 'correct' in d:
					if d['correct']:
						judgement.score = 1
					if not d['correct']:
						judgement.score = -1
	judgement.save()
	log.debug('judgement saved: '+str(judgement)+' with score: '+str(judgement.score)) 
	return judgement