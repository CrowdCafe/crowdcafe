from django import forms
from datetime import date, timedelta
from models import Job, Task, DataItem
from qualitycontrol.models import QualityControl
from qualitycontrol.models import DEVICES_ALLOWED

from models import STATUS_CHOISE
from django.conf import settings

from django.contrib.auth.models import User
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, Layout

import logging
from decimal import Decimal
from django.utils.datetime_safe import datetime
from django.forms.forms import Form
from django.forms.fields import FileField
from utils import getGithubRepositoryFiles

log = logging.getLogger(__name__)

class JobForm(ModelForm):

	owner = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
	title = forms.CharField(label=(u'Title'))
	description = forms.CharField(label=(u'Description'), widget=forms.Textarea())
	webhook_url = forms.URLField(label='Webhook', required=False)
	status = forms.ChoiceField(choices=STATUS_CHOISE, widget=forms.Select(), initial = 'NP', label=(u'Status'), required=False)
	category = forms.ChoiceField(choices=settings.TASK_CATEGORIES_DICTIONARY, initial = 'ZT', widget=forms.Select(), label=(u'Category'), required=False)
	template_url = forms.ChoiceField(choices=getGithubRepositoryFiles('.html'), widget=forms.Select(), label=(u'User Interface'), required=True)
	class Meta:
		model = Job
		exclude = ('date_deadline','date_created','template_html')
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))
		self.helper.form_class = 'form-vertical'
		self.helper.layout = Layout(Fieldset('Job','title', 'description','template_url','category','status','webhook_url','owner'))
		super(JobForm, self).__init__(*args, **kwargs)

class QualityControlForm(ModelForm):

	job = forms.ModelChoiceField(queryset=Job.objects.all(), widget=forms.HiddenInput)
	min_confidence = forms.IntegerField(label=(u'Minimum confidence level'))

	gold_min = forms.IntegerField(label=(u'Minimum amount of gold per task'))
	gold_max = forms.IntegerField(label=(u'Maximum amount of gold per task'))
	score_min = forms.IntegerField(label=(u'Minimum score to be allowed to work further'))
	dataitems_per_task = forms.IntegerField(label=(u'Dataitems in one task'))
	min_answers_per_item = forms.IntegerField(label=(u'Amount of answers to be collected per each dataunit'))
	max_dataitems_per_worker = forms.IntegerField(label=(u'Max dataunits per worker'))
	device_type = forms.ChoiceField(choices=DEVICES_ALLOWED, widget=forms.Select(), initial = 0, label=(u'Device allowed'), required=False)
	
	qualitycontrol_url = forms.URLField(label=(u'URL which is called to do quality check'), required=False)

	class Meta:
		model = QualityControl
		exclude = ('min_confidence')
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))
		self.helper.form_class = 'form-vertical'
		self.helper.layout = Layout(Fieldset('Quality Control','job', 'gold_min','gold_max','score_min','dataitems_per_task','min_answers_per_item','max_dataitems_per_worker','device_type','qualitycontrol_url'))
		super(QualityControlForm, self).__init__(*args, **kwargs)