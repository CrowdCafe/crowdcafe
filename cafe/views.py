from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from kitchen.models import Job, Unit, Judgement
#from kitchen.models import getPlatformOwner, calculateCommission

#from preselection.models import Preselection
#from preselection.utils import qualifiedJob

from rewards.models import Vendor, Reward, Coupon

from account.models import FundTransfer
from events.utils import logEvent

from random import randint
import json
import random
from random import shuffle
from mobi.decorators import detect_mobile


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
	coupons = Coupon.objects.filter(account = request.user.profile.personalAccount, status = 'AV').order_by('-date_updated').all()
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

def Home(request):
	if request.user.is_authenticated():
		logEvent(request, 'home')
		return render_to_response('cafe/home/pages/home.html', context_instance=RequestContext(request))
	else:
		return redirect('cafe-welcome')

@detect_mobile
@login_required 
def JobList(request):
	jobs = Job.objects.filter(status = 'PB')
	if 'category' in request.GET:
		jobs = jobs.filter(category = request.GET['category'])
	jobs = jobs.order_by('-date_created').all()
	jobs_available = jobs
	#for job in jobs:
	#	if userIsQualifiedForJob(job, request.user, request.mobile):
	#		jobs_available.append(job)

	logEvent(request, 'joblist')
	return render_to_response('cafe/home/pages/joblist.html', {'jobs':jobs_available}, context_instance=RequestContext(request))

# -----------------------------------
# Units related views
# -----------------------------------
@login_required 
def UnitsAssign(request, job_id):
	job = get_object_or_404(Job, pk = job_id)

	# if this job is published or the current user is its creator	
	if job.status == 'PB' or job.creator == request.user:
		# get a subset of data units (the amount defined in job.units_per_page)
		units = job.assignUnits(request.user)
		if units:
			return render_to_response('cafe/home/pages/job.html', {'job':job,'units':units}, context_instance=RequestContext(request))
	
	return redirect(reverse('cafe-job-list')+'?category='+job.category)

@login_required 
def UnitsComplete(request, job_id): 
	job = get_object_or_404(Job, pk = job_id, status = 'PB')
	
	# get list of units which are executed in the task form, which has status "Not Completed" and are published
	units = []
	if 'unit_ids' in request.POST:
		unit_ids_pool = request.POST['unit_ids']
		units_query = Unit.objects.filter(status = 'NC', published = True)

		if type(unit_ids_pool).__name__ == 'list':
			units = units_query.filter(pk__in = unit_ids_pool).all()
		else:
			units = units_query.filter(pk = unit_ids_pool).all()
	
	# go through all the POST data for each unit and save relative data to judgement
	judgements = []
	for unit in units:
		judgements.append(unit.saveJudgement(request.POST,request.user))
	# send a request to URL defined in job settings with info about judgements provided
	job.webhook(judgements)
	return redirect(reverse('cafe-units-assign', kwargs={'job_id': job.id})+'?completed_previous=1')

# -----------------------------------
# Rewards related views
# -----------------------------------
@login_required 
def RewardPurchase(request, reward_id):

	reward = get_object_or_404(Reward,pk = reward_id)
	coupons = Coupon.objects.filter(reward = reward, status = 'NA')
	
	if coupons.count()>0 and request.user.profile.account.balance >= reward.cost:
		
		transaction = AccountTransaction(currency = 'VM', to_account = reward.owner.profile.account, from_account = request.user.profile.account, amount = reward.cost, description = 'reward '+reward.title)
		transaction.save()
		
		assignedcoupon = coupons.all()[0]
		assignedcoupon.status = 'AC'
		assignedcoupon.worker = request.user
		assignedcoupon.transaction = transaction

		assignedcoupon.save()
		logEvent(request, 'coupon_purchased',assignedcoupon.reward.id, assignedcoupon.id)
	else:
		logEvent(request, 'coupon_not_purchased')
	
	return redirect('cafe-rewards')

@login_required 
def CouponActivate(request, coupon_id):

	coupon = get_object_or_404(Coupon, pk = coupon_id, worker = request.user, status = 'AC')
	coupon.status = 'PS'
	coupon.save()
	
	logEvent(request, 'coupon_activated',coupon.reward.id, coupon.id)
	return redirect('cafe-rewards')

