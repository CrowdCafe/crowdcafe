from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from models import Job, Task, DataItem
from social_auth.models import UserSocialAuth
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage as s3_storage
from preselection.models import Preselection

import re
import csv
import urllib2
import StringIO
import scraperwiki 


from utils import getGithubRepositoryFiles, saveDataItems, collectDataFromCSV,collectDataFromSocialNetwork,collectDataFromTwitter,simplifyInstagramDataset,collectDataFromInstagram

#import jobs

#def test_celery(request):
#	result = jobs.sleepjob.delay(10)
#	result_one = jobs.sleepjob.delay(10)
#	result_two = jobs.sleepjob.delay(10)
#	return HttpResponse(result.job_id)

@login_required
def Home(request):
	jobs = Job.objects.filter(owner = request.user).exclude(status='DL').order_by('-date_created').all()
	return render_to_response('kitchen/home.html', {'jobs':jobs}, context_instance=RequestContext(request))

@login_required
def JobData(request, job_id):
	job = get_object_or_404(Job,pk = job_id, owner = request.user)
	dataitems = DataItem.objects.filter(job = job)
	return render_to_response('kitchen/dataitems.html', {'dataitems':dataitems,'job':job}, context_instance=RequestContext(request))

@login_required
def JobNew(request):
	extention = '.html'

	html_templates = getGithubRepositoryFiles(extention)
	
	return render_to_response('kitchen/newjob.html', {'html_templates':html_templates}, context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def JobStatusChange(request, job_id, status):

	job = get_object_or_404(Job,pk = job_id, owner = request.user)
	job.status = status
	job.save()
	return redirect('kitchen-home')
	
@login_required
def JobSave(request):

	template_url = request.POST['userinterface_template']
	template_html = urllib2.urlopen(template_url).read()
	# -----------------------
	# job creation
	# -----------------------
	new_job = Job(
		owner = request.user, 
		title = request.POST['job_title'],
		description = request.POST['job_description'],
		dataitems_per_task = int(request.POST['dataitems_per_task']),
		min_answers_per_item = int(request.POST['min_answers_per_item']),
		#min_confidence = int(request.POST['min_confidence']),
		#template = request.POST['ui_type'],
		category = request.POST['job_category'],
		template_html  = template_html,
		template_url = template_url
	)
	if 'min_confidence' in request.POST:
		new_job.min_confidence = int(request.POST['min_confidence'])
	if 'webhook_url' in request.POST:
		new_job.webhook_url = request.POST['webhook_url']
	new_job.save()
	# -----------------------
	# Preselection
	# -----------------------
	
	i = 0
	if 'preselection_rule' in request.POST:
		for rule in request.POST.getlist('preselection_rule'):
			related_job = get_object_or_404(Job,pk = request.POST.getlist('preselection_job')[i])
			rule_type = request.POST.getlist('preselection_rule')[i]
			new_rule = Preselection(job = new_job, rule_type = rule_type, related_job = related_job)
			new_rule.save()
			i+=1

	# -----------------------
	# Data
	# -----------------------
	dataset = []

	dataset_option = request.POST['dataset_option_selected']
	#if dataset_option == 'api' - do nothing
	if dataset_option == 'survey':
		dataset = [{'no data':'survey'}]
	
	elif dataset_option == 'dataset':
		if request.FILES:
			if 'dataset' in request.FILES:
				new_job.dataset_file.save(str(new_job.id)+request.FILES['dataset'].name, request.FILES['dataset'])
				new_job.save()
				dataset = collectDataFromCSV(new_job.dataset_file.url)
	
	elif dataset_option == 'feed':	
		keyword = request.POST['feed_handler']
		amount = int(request.POST['feed_amount'])
		feed_type = int(request.POST['feed-type'])

		if feed_type == 0: # Twitter
			dataset = collectDataFromTwitter(keyword, amount)
		if feed_type == 2: # Instagram
			dataset = simplifyInstagramDataset(collectDataFromInstagram(keyword, amount))
	
	saveDataItems(new_job,dataset)
	return redirect('kitchen-home')
