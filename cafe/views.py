from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from kitchen.models import Job, Unit, Judgement
from kitchen.webhooks import webhook_results, webhook_quality_conrol, saveJudgements
from django.views.generic.list import ListView

from rewards.models import Vendor, Reward, Coupon

from account.models import FundTransfer
from events.utils import logEvent

from random import randint
import json
import random
from random import shuffle
from mobi.decorators import detect_mobile

def Home(request):
	if request.user.is_authenticated():
		logEvent(request, 'home')
		return render_to_response('cafe/home/pages/home.html', context_instance=RequestContext(request))
	else:
		return redirect('cafe-welcome')

def Welcome(request):
	if request.user.is_authenticated():
		return redirect('cafe-home')

	logEvent(request, 'welcome')
	return render_to_response('cafe/home/pages/welcome.html', context_instance=RequestContext(request))

def About(request):
	logEvent(request, 'about')
	return render_to_response('cafe/home/pages/about.html', context_instance=RequestContext(request))

@login_required 
def Rewards(request):
	logEvent(request, 'rewards')
	# show available rewards
	coupons = Coupon.objects.filter(account = request.user.profile.personalAccount, status = 'AC').order_by('-date_updated').all()
	vendors = Vendor.objects.all()
	
	return render_to_response('cafe/home/pages/rewards.html', {'vendors':vendors, 'coupons':coupons}, context_instance=RequestContext(request))

@login_required
def UserProfile(request):
	target_user = {}
	if 'user' in request.GET:
		users = User.objects.filter(pk = int(request.GET['user']))
		if users.count()>0:

			target_user = users.get()
			stats = {}
			stats['completed'] = Judgement.objects.filter(worker = target_user).count()
			stats['published'] = Job.objects.filter(creator = target_user).count()

	return render_to_response('cafe/home/pages/profile.html', {'target_user':target_user, 'stats':stats}, context_instance=RequestContext(request))

@login_required 
def Transactions(request):
	logEvent(request, 'transactions')
	return render_to_response('cafe/home/pages/transactions.html', context_instance=RequestContext(request))


@login_required 
def setContext(request):
	if 'context' in request.GET:
		context = request.GET['context']

	request.session['cafe-context'] = context
	logEvent(request, 'context_change')
	return HttpResponse({json.dumps({'context':context})}, content_type="application/json")



class JobListView(ListView):
	model = Job
	template_name = "cafe/home/pages/job_list.html"

	def get_queryset(self):
		#TODO simplify this
		jobs = Job.objects.filter(status = 'PB')
		if 'category' in self.request.GET:
			jobs = jobs.filter(category = self.request.GET['category'])
		jobs_ids_pool = []
		for job in jobs:
			if job.assignUnits(self.request.user):
				jobs_ids_pool.append(job.id)
		print jobs_ids_pool
		return Job.objects.filter(id__in = jobs_ids_pool).order_by('-date_created')

	def get_context_data(self, **kwargs):
		context = super(JobListView, self).get_context_data(**kwargs)
		return context

# -----------------------------------
# Units related views
# -----------------------------------
@login_required 
def UnitsAssign(request, job_id):
	job = get_object_or_404(Job, pk = job_id)

	# if this job is published or the current user is its creator	
	if job.status == 'PB' or job.creator == request.user:
		gold_creation = False 
		# if the current user is a member of the job app account and there is an http parameter that this is a gold_creation task
		if 'gold_creation' in request.GET:
			gold_creation = bool(request.GET['gold_creation'])
		# get a subset of data units (the amount defined in job.units_per_page)
		units = job.assignUnits(request.user, gold_creation)
		if units:
			return render_to_response('cafe/home/pages/job.html', {'job':job,'units':units,'gold_creation':int(gold_creation)}, context_instance=RequestContext(request))
	
	return redirect(reverse('cafe-job-list')+'?completed_previous=0&category='+job.category)

@login_required 
def UnitsComplete(request, job_id): 
	job = get_object_or_404(Job, pk = job_id, status = 'PB')
		# get list of units which are executed in the task form, which has status "Not Completed" and are published
	units = []
	gold_creation = False
	if 'gold_creation' in request.POST and int(request.POST['gold_creation'])==1:
		gold_creation = True
	
	units_pool_handler = 'unit_ids' # pool with a list of unit ids completed in this task
	if units_pool_handler in request.POST:
		unit_ids_pool = request.POST.getlist(units_pool_handler)
		units_query = Unit.objects.filter(status = 'NC', published = True)
		units = units_query.filter(pk__in = unit_ids_pool).all()
	# go through all the POST data for each unit and save relative data to judgement
	saveJudgements(units, request.POST, request.user, gold_creation)
	get_url = '?completed_previous=1'
	if gold_creation:
		get_url+='&gold_creation=1'
	return redirect(reverse('cafe-units-assign', kwargs={'job_id': job.id})+get_url)

# -----------------------------------
# Rewards related views
# -----------------------------------
@login_required 
def RewardPurchase(request, reward_id):

	reward = get_object_or_404(Reward,pk = reward_id)
	coupon = reward.purchaseCoupon(request.user)
	if coupon:
		logEvent(request, 'coupon_purchased',coupon.reward.id, coupon.id)
	else:
		logEvent(request, 'coupon_not_purchased')
	return redirect('cafe-rewards')

@login_required 
def CouponActivate(request, coupon_id):

	coupon = get_object_or_404(Coupon, pk = coupon_id, account = request.user.profile.personalAccount, status = 'AC')
	coupon.status = 'UD'
	coupon.save()
	
	logEvent(request, 'coupon_activated',coupon.reward.id, coupon.id)
	return redirect('cafe-rewards')

