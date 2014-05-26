from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from kitchen.models import Job, Task, Answer, AnswerItem, DataItem
from kitchen.models import getPlatformOwner, calculateCommission

from preselection.models import Preselection
from preselection.utils import qualifiedJob

from rewards.models import Vendor, Reward, Coupon

from account.models import AccountTransaction
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
	coupons = Coupon.objects.filter(worker = request.user, status = 'AC').order_by('-date_updated').all()
	vendors = Vendor.objects.all()
	
	return render_to_response('cafe/home/pages/rewards.html', {'vendors':vendors, 'coupons':coupons}, context_instance=RequestContext(request))

@login_required
def UserProfile(request):
	profile = {}
	if 'user' in request.GET:
		users = User.objects.filter(pk = int(request.GET['user']))
		if users.count()>0:

			profile = users.get()
			stats = {}
			stats['completed'] = Answer.objects.filter(executor = profile).count()
			stats['published'] = Job.objects.filter(owner = profile).count()
			#stats['execution'] = 


	return render_to_response('cafe/home/pages/profile.html', {'profile':profile, 'stats':stats}, context_instance=RequestContext(request))

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
	jobs = Job.objects.filter(status = 'ST')
	if 'category' in request.GET:
		jobs = jobs.filter(category = request.GET['category'])
	jobs = jobs.order_by('-date_created').all()
	jobs_available = []
	for job in jobs:
		if userIsQualifiedForJob(job, request.user, request.mobile):
			jobs_available.append(job)

	logEvent(request, 'joblist')
	return render_to_response('cafe/home/pages/joblist.html', {'jobs':jobs_available}, context_instance=RequestContext(request))

@login_required 
def JobAssign(request, job_id):
	job = get_object_or_404(Job, pk = job_id)
	if job.status == 'ST' or job.owner == request.user: 
		assigned_task = generateTask(job,request.user)

		#tasks = tasksAvailableExist(job,request.user)
		completed_previous = '0'
		if assigned_task:
			#assigned_task = tasks.all()[randint(0,tasks.count()-1)]
			if 'completed_previous' in request.GET:
				completed_previous = str(int(request.GET['completed_previous']))
			logEvent(request, 'task_assigned',assigned_task.job.id, assigned_task.id)
			return redirect(reverse('cafe-task-execute', kwargs={'task_id': assigned_task.id})+'?completed_previous='+completed_previous)

	logEvent(request, 'task_not_assigned',job_id)
	return redirect('cafe-job-list')

@login_required 
def TaskExecute(request, task_id): 
	if Task.objects.filter(status = 'ST', pk = task_id).count() >0 and Answer.objects.filter(executor = request.user, task__id = task_id).count() == 0:
		task = get_object_or_404(Task, pk = task_id)
		logEvent(request, 'execution_started',task.job.id, task.id)
		return render_to_response('cafe/home/pages/job.html', {'task':task}, context_instance=RequestContext(request))
	else:
		return redirect('cafe-home')

@login_required 
def AccountRemove(request, account_id): 
	request.user.profile.removeConnectedSocialNetwork(account_id)
	return redirect(reverse('cafe-profile')+'?user='+str(request.user.id))

@login_required 
def TaskSkip(request, task_id): 
	task = get_object_or_404(Task, pk = task_id)
	tasks = tasksAvailableExist(task.job,request.user, task.id)

	logEvent(request, 'execution_skipped', task.job.id, task.id)
	if tasks:
		assigned_task = tasks.all()[randint(0,tasks.count()-1)]

		return redirect(reverse('cafe-task-execute', kwargs={'task_id': assigned_task.id}))
	else:
		return redirect('cafe-job-list')
	
@login_required 
def TaskComplete(request, task_id): 
	task = get_object_or_404(Task, pk = task_id)

	if Answer.objects.filter(task = task, executor = request.user).count() == 0:
		new_answer = Answer(task=task, executor = request.user, status = 'FN')
		new_answer.save()

		for dataitem in task.items:
			answer_item_value = {}
			score = 0.0
			for key in request.POST:
				dataitem_handle = 'dataitem_'+str(dataitem.id)
				if dataitem_handle in key:
					answer_item_value[key.replace(dataitem_handle,'')] = request.POST[key]
					print dataitem.gold
					if dataitem.gold and 'gold'+key.replace(dataitem_handle,'') in dataitem.value:
						if request.POST[key] == dataitem.value['gold'+key.replace(dataitem_handle,'')]:
							score+=1.0
						else:
							score-=1.0
			new_answer_item = AnswerItem(answer = new_answer,dataitem = dataitem, value = answer_item_value, score = score)
			new_answer_item.save()
			new_answer_item.dataitem.refreshStatus()
		new_answer.webhook()
		if len(task.answers) >= task.job.qualitycontrol.min_answers_per_item:
			task.status = 'FN'
			task.save()

		logEvent(request, 'execution_completed',task.job.id, task.id)

	else:
		logEvent(request, 'execution_completed_withmistake_notsaved',task.job.id, task.id)
	return redirect(reverse('cafe-job-assign', kwargs={'job_id': task.job.id})+'?completed_previous=1')


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

def generateTask(job,user):

	score = job.qualitycontrol.score(user)
	# if the current score is not False (did not work on a task yet) or is higher than the allowed in quality control
	if job.qualitycontrol.allowed_to_work_more(user):
		# get a list of available not gold dataitems
		dataitems_regular = availableDataItems(job, user, False)
		# get a list of available gold dataitems
		dataitems_gold = availableDataItems(job, user, True)
		
		
		if score > job.qualitycontrol.gold_max:
			gold_amount_to_put = 0
		if score > job.qualitycontrol.gold_min and score <= job.qualitycontrol.gold_max:
			gold_amount_to_put = max([score - job.qualitycontrol.gold_min,job.qualitycontrol.gold_min])
		if score <= job.qualitycontrol.gold_min:
			gold_amount_to_put = job.qualitycontrol.gold_max

		dataitems_to_put = []
		if dataitems_regular:
			gold_amount_to_put = 0
			regular_amount_to_put = 0
			if dataitems_gold:
				if score > job.qualitycontrol.gold_max:
					gold_amount_to_put = job.qualitycontrol.gold_min
				if score > job.qualitycontrol.gold_min and score <= job.qualitycontrol.gold_max:
					gold_amount_to_put = max([job.qualitycontrol.gold_max - score,job.qualitycontrol.gold_min])
				if score <= job.qualitycontrol.gold_min:
					gold_amount_to_put = job.qualitycontrol.gold_max

				gold_amount_to_put = min([dataitems_gold.count(), int(gold_amount_to_put)])
				dataitems_to_put = random.sample(dataitems_gold.all(), gold_amount_to_put) 

			regular_amount_to_put = min([dataitems_regular.count(),int(job.qualitycontrol.dataitems_per_task - gold_amount_to_put)]) 
			dataitems_to_put += random.sample(dataitems_regular.all(), regular_amount_to_put)
			shuffle(dataitems_to_put)
			
			task = Task(job=job)
			task.save()
			task.dataitems.add(*dataitems_to_put)
			task.save()
			return task
	return False

def userIsQualifiedForJob(job,user, mobile):
	if availableDataItems(job, user) and job.qualitycontrol.allowed_to_work_more(user) and qualifiedJob(job,user) and (job.qualitycontrol.device_type == 0 or (mobile and job.qualitycontrol.device_type == 1) or (not mobile and job.qualitycontrol.device_type == 2)):
		return True
	else:
		print job.id
		print availableDataItems(job, user)
		print job.qualitycontrol.allowed_to_work_more(user)
		print qualifiedJob(job,user)
		return False

def availableDataItems(job, user, gold = False):

	dataitems_already_did = AnswerItem.objects.filter(answer__executor = user, dataitem__job = job).values('dataitem')
	dataitems_available = DataItem.objects.filter(job = job, status = 'NR', gold = gold).exclude(pk__in = dataitems_already_did)

	if dataitems_available.count()>0:
		return dataitems_available
	else:
		return False