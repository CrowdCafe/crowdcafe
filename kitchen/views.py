from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.conf import settings
from models import Task, TaskInstance, DataItem
from social_auth.models import UserSocialAuth

from firebase import Firebase
from django.core.files.storage import default_storage as s3_storage

import re
import csv
import urllib2
import StringIO
import scraperwiki 

from apiTwitter import TwitterCall
#import tasks

def test_celery(request):
	result = tasks.sleeptask.delay(10)
	result_one = tasks.sleeptask.delay(10)
	result_two = tasks.sleeptask.delay(10)
	return HttpResponse(result.task_id)

@login_required
def Home(request):

	tasks = Task.objects.filter(owner = request.user).exclude(status='DL').order_by('-date_created').all()
	return render_to_response('kitchen/home.html', {'tasks':tasks}, context_instance=RequestContext(request))

@login_required
def TaskNew(request):
	return render_to_response('kitchen/task.html', context_instance=RequestContext(request))

@login_required
def TaskDelete(request, task_id):

	task = get_object_or_404(Task,pk = task_id, owner = request.user)
	task.status = 'DL'
	task.save()
	return redirect('kitchen-home')

@login_required
def TaskSave(request):

	print request.FILES
	template_url = request.POST['userinterface_template']
	template_html = urllib2.urlopen(template_url).read()

	new_task = Task(
		owner = request.user, 
		title = request.POST['task_title'],
		description = request.POST['task_description'],
		dataitems_per_instance = int(request.POST['dataitems_per_instance']),
		min_answers_per_item = int(request.POST['min_answers_per_item']),
		min_confidence = int(request.POST['min_confidence']),
		template = request.POST['ui_type'],
		template_html  = template_html,
		template_url = template_url
	)
	new_task.save()

	dataset = []

	# -----------------------
	dataset_option = request.POST['dataset_option_selected']
	if dataset_option == 'survey':
		dataset = [{'no data':'survey'}]
	elif dataset_option == 'dataset':
		if request.FILES:
			if 'dataset' in request.FILES:
				new_task.dataset_file.save(str(new_task.id)+request.FILES['dataset'].name, request.FILES['dataset'])
				new_task.save()
				dataset = collectDataFromCSV(new_task.dataset_file.url)
	elif dataset_option == 'feed':	
		dataset = collectDataFromTwitter(request.POST['feed_handler'], int(request.POST['feed_amount']))	
	
	if len(dataset)>0:
		createTaskInstances(new_task,dataset)

	return redirect('kitchen-home')

def createTaskInstances(task,dataset):
	i = 0
	for item in dataset:
		if i % task.dataitems_per_instance == 0:
			taskinstance = TaskInstance(task=task)
			taskinstance.save()
		dataitem = DataItem(taskinstance = taskinstance, value = item)
		dataitem.save()
		i+=1

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

def collectDataFromTwitter(keyword, amount):
	instance = UserSocialAuth.objects.filter(provider='twitter')[0]

	TWITTER_ACCESS_TOKEN = (instance.tokens).get('oauth_token')
	TWITTER_ACCESS_TOKEN_SECRET = (instance.tokens).get('oauth_token_secret')
	
	apicall=TwitterCall(client_id=TWITTER_ACCESS_TOKEN,client_secret=TWITTER_ACCESS_TOKEN_SECRET)
	
	dataset = apicall.getByKeyword(keyword, amount, False)
	return dataset