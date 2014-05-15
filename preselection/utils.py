from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.conf import settings

from kitchen.models import Job, Task, DataItem, Answer, AnswerItem
from models import Preselection

# Check whether the user satisfies a particular rule
def qualifiedPreselection(preselection, user):
	answers = Answer.objects.filter(executor = user, task__job = preselection.related_job, status = 'FN')
	if (preselection.rule_type == 'WO' and answers.count() > 0) or (preselection.rule_type == 'NW' and answers.count() == 0):
		return True
	else:
		return False

# Check whether the user satisfies all preselection rules of a task
def qualifiedJob(job, user):
	qualified = True

	for preselection in job.preselection_set.all():
		if not qualifiedPreselection(preselection, user):
			qualified = False
	return qualified