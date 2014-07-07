from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from models import Attachment
from kitchen.models import Job
from account.models import Account
from rewards.models import Reward

from social_auth.models import UserSocialAuth
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage as s3_storage

from forms import AttachmentForm

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

import logging

import re
import csv
import urllib2
import StringIO

from utils import collectDataFromCSV, saveUnits, generateCoupons
log = logging.getLogger(__name__)

# -------------------------------------------------------------
# Job Attachment
# -------------------------------------------------------------
class AttachmentCreateView(CreateView):
	model = Attachment
	template_name = "kitchen/crispy.html"
	form_class = AttachmentForm

	def get_initial(self):
		initial = {}
		initial['job'] = get_object_or_404(Job,pk = self.kwargs.get('job_pk', None))
		return initial
	
	def form_invalid(self, form):
		log.debug("form is not valid")
		return CreateView.form_invalid(self, form)

	def form_valid(self, form):
		log.debug("saved")
		attachment = form.save()
		attachment.save()
		# Parse csv to array of units, add these units to the job
		saveUnits(attachment.job,collectDataFromCSV(attachment.source_file.url))

		return redirect(reverse('unit-list', kwargs={'job_pk': attachment.job.id}))

def generateRewardCoupons(request, reward_pk):
	reward = get_object_or_404(Reward, pk = reward_pk, vendor__account__users__in=[request.user.id])
	generateCoupons(reward, 5)

	return redirect(reverse('coupon-list', kwargs={'reward_pk': reward.id}))

