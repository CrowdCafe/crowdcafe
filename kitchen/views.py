from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from models import Job, Task, DataItem, Attachment, Answer
from qualitycontrol.models import QualityControl
from social_auth.models import UserSocialAuth
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage as s3_storage
from preselection.models import Preselection

from forms import JobForm,QualityControlForm

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

import logging

import re
import csv
import urllib2
import StringIO
import scraperwiki 

log = logging.getLogger(__name__)

from utils import getGithubRepositoryFiles, saveDataItems, collectDataFromCSV,collectDataFromSocialNetwork,collectDataFromTwitter,simplifyInstagramDataset,collectDataFromInstagram

def JobDataUpload(request, pk):
	job = get_object_or_404(Job,pk = pk, owner =request.user)

	# -----------------------
	# Input dataset
	# -----------------------
	dataset = []
	if 'dataset_option_selected' in request.POST:
		dataset_option = request.POST['dataset_option_selected']
		if dataset_option == 'survey':
			dataset = [{'no data':'survey'}]
		elif dataset_option == 'dataset':
			if request.FILES:
				if 'dataset' in request.FILES:
				
					dataset_file = Attachment(job = job)
					dataset_file.file.save(str(job.id)+request.FILES['dataset'].name, request.FILES['dataset'])
					dataset_file.save()
					
					dataset = collectDataFromCSV(dataset_file.file.url)
		
		elif dataset_option == 'feed' and request.POST['feed_handler'] and request.POST['feed_amount'] and request.POST['feed-type']:	
			keyword = request.POST['feed_handler']
			amount = int(request.POST['feed_amount'])
			feed_type = int(request.POST['feed-type'])
			if feed_type == 0: # Twitter
				dataset = collectDataFromTwitter(keyword, amount)
			if feed_type == 2: # Instagram
				dataset = simplifyInstagramDataset(collectDataFromInstagram(keyword, amount))
	
		saveDataItems(job,dataset)
	return redirect(reverse('kitchen-job-data', kwargs={'pk': job.id}))
class JobCreation(CreateView):
	model = Job
	template_name = "kitchen/crispy.html"
	form_class = JobForm
	print 1

	def get_initial(self):
		initial = {}
		initial['owner'] = self.request.user
		return initial
	
	def form_invalid(self, form):
		log.debug("form is not valid")
		print (form.errors)
		return CreateView.form_invalid(self, form)

	def form_valid(self, form):
		log.debug("saved")
		job = form.save()
		job.save()
		quality = QualityControl(job = job)
		quality.save()

		return redirect(reverse('kitchen-job-data', kwargs={'pk': job.id}))

class JobUpdate(UpdateView):
	model = Job
	template_name = "kitchen/crispy.html"
	form_class = JobForm

	def get_initial(self):
		initial = {}
		initial['owner'] = self.request.user
		return initial

	def get_success_url(self):
		return reverse_lazy('kitchen-home')
	def form_invalid(self, form):
		log.debug("form is not valid")
		print (form.errors)
		return CreateView.form_invalid(self, form)
	def get_queryset(self):
		return Job.objects.filter(pk=self.kwargs.get('pk', None),owner = self.request.user) # or request.POST
	def form_valid(self, form):
		log.debug("updated")
		job = form.save()
		return HttpResponseRedirect(self.get_success_url())

class QualityControlUpdate(UpdateView):
	model = QualityControl
	template_name = "kitchen/crispy.html"
	form_class = QualityControlForm

	def get_initial(self):
		initial = {}
		return initial

	def get_success_url(self):
		return reverse_lazy('kitchen-home')
	def form_invalid(self, form):
		log.debug("form is not valid")
		print (form.errors)
		return CreateView.form_invalid(self, form)
	def get_queryset(self):
		return QualityControl.objects.filter(pk=self.kwargs.get('pk', None), job__owner = self.request.user) # or request.POST
	def form_valid(self, form):
		log.debug("updated")
		form.save()
		return HttpResponseRedirect(self.get_success_url())

@login_required
def Home(request):
	jobs = Job.objects.filter(owner = request.user).exclude(status='DL').order_by('-date_created').all()
	return render_to_response('kitchen/home.html', {'jobs':jobs}, context_instance=RequestContext(request))

@login_required
def JobData(request, pk):
	job = get_object_or_404(Job,pk = pk, owner = request.user)
	dataitems = DataItem.objects.filter(job = job)
	return render_to_response('kitchen/job/dataitems.html', {'dataitems':dataitems,'job':job}, context_instance=RequestContext(request))

@login_required
def JobWorkers(request, pk):
	job = get_object_or_404(Job,pk = pk, owner = request.user)
	answers = Answer.objects.filter(task__job = job, status = 'FN').order_by('executor').order_by('-date_created')
	return render_to_response('kitchen/job/answers.html', {'answers':answers,'job':job}, context_instance=RequestContext(request))

@login_required
def JobSave(request):

	template_url = request.POST['userinterface_template']
	# -----------------------
	# Job creation
	# -----------------------
	new_job = Job(
		owner = request.user, 
		title = request.POST['job_title'],
		description = request.POST['job_description'],
		category = request.POST['job_category'],
		template_url = template_url
	)
	
	if 'webhook_url' in request.POST:
		new_job.webhook_url = request.POST['webhook_url']

	new_job.save()
	new_job.refresh_template()
	# -----------------------
	# Quality control
	# -----------------------
	new_quality_control = QualityControl(
		job = new_job,
		gold_min = int(request.POST['min_gold_per_task']),
		gold_max = int(request.POST['max_gold_per_task']),
		score_min = float(request.POST['min_score']),
		dataitems_per_task = int(request.POST['dataitems_per_task']),
		min_answers_per_item = int(request.POST['min_answers_per_item']),
		device_type = int(),
		max_dataitems_per_worker = float(request.POST['max_dataitems_per_worker'])
		)

	if 'min_confidence' in request.POST:
		new_quality_control.min_confidence = int(request.POST['min_confidence'])
	new_quality_control.save()
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
	# Input dataset
	# -----------------------
	dataset = []

	dataset_option = request.POST['dataset_option_selected']
	#if dataset_option == 'api' - do nothing
	if dataset_option == 'survey':
		dataset = [{'no data':'survey'}]
	
	elif dataset_option == 'dataset':
		if request.FILES:
			if 'dataset' in request.FILES:
				
				dataset_file = Attachment(job = new_job)
				dataset_file.file.save(str(new_job.id)+request.FILES['dataset'].name, request.FILES['dataset'])
				dataset_file.save()
				
				dataset = collectDataFromCSV(dataset_file.file.url)
	
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
