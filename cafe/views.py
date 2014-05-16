from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from kitchen.models import Task, TaskInstance, Answer, AnswerItem, DataItem, MaxResponses
from kitchen.models import getPlatformOwner, calculateCommission

from preselection.models import Preselection
from preselection.utils import qualifiedTask

from rewards.models import Vendor, Reward, Coupon

from account.models import AccountTransaction
from events.utils import logEvent

from random import randint
import json

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
	#return render_to_response('cafe/home/pages/transactions.html', context_instance=RequestContext(request))


def Home(request):
	if request.user.is_authenticated():
		logEvent(request, 'home')
		return render_to_response('cafe/home/pages/home.html', context_instance=RequestContext(request))
	else:
		return redirect('cafe-welcome')

@login_required 
def TaskList(request):
	max = MaxResponses
	if max > 0:
		tasks = Task.objects.filter(status = 'ST')
		if 'category' in request.GET:
			tasks = tasks.filter(category = request.GET['category'])
		tasks = tasks.order_by('-date_created').all()
		tasks_available = []
		for task in tasks:
			if instancesAvailableExist(task,request.user) and qualifiedTask(task,request.user):
				tasks_available.append(task)
		logEvent(request, 'tasklist')
	return render_to_response('cafe/home/pages/tasklist.html', {'tasks':tasks_available}, context_instance=RequestContext(request))

@login_required 
def TaskInstanceAssign(request, task_id):
	task = get_object_or_404(Task, pk = task_id)
	if task.status == 'ST' or task.owner == request.user: 
		instances = instancesAvailableExist(task,request.user)
		completed_previous = '0'

		if 'completed_previous' in request.GET:
			completed_previous = str(int(request.GET['completed_previous']))

		if instances:
			assigned_instance = instances.all()[randint(0,instances.count()-1)]

			logEvent(request, 'instance_assigned',assigned_instance.task.id, assigned_instance.id)
			return redirect(reverse('cafe-taskinstance-execute', kwargs={'instance_id': assigned_instance.id})+'?completed_previous='+completed_previous)

	logEvent(request, 'instance_not_assigned',task_id)
	return redirect('cafe-task-list')

@login_required 
def TaskInstanceExecute(request, instance_id): 
	if TaskInstance.objects.filter(status = 'ST', pk = instance_id).count() >0 and Answer.objects.filter(executor = request.user, taskinstance__id = instance_id).count() == 0:
		taskinstance = get_object_or_404(TaskInstance, pk = instance_id)
		logEvent(request, 'execution_started',taskinstance.task.id, taskinstance.id)
		return render_to_response('cafe/home/pages/task.html', {'taskinstance':taskinstance}, context_instance=RequestContext(request))
	else:
		return redirect('cafe-home')
	

@login_required 
def TaskInstanceSkip(request, instance_id): 
	instance = get_object_or_404(TaskInstance, pk = instance_id)
	instances = instancesAvailableExist(instance.task,request.user, instance.id)

	logEvent(request, 'execution_skipped', instance.task.id, instance.id)
	if instances:
		assigned_instance = instances.all()[randint(0,instances.count()-1)]

		return redirect(reverse('cafe-taskinstance-execute', kwargs={'instance_id': assigned_instance.id}))
	else:
		return redirect('cafe-task-list')
	
@login_required 
def TaskInstanceComplete(request, instance_id): 
	taskinstance = get_object_or_404(TaskInstance, pk = instance_id)

	if Answer.objects.filter(taskinstance = taskinstance, executor = request.user).count() == 0:
		new_answer = Answer(taskinstance=taskinstance, executor = request.user, status = 'FN')
		new_answer.save()

		for dataitem in taskinstance.dataitems:
			answer_item_value = {}
			for key in request.POST:
				dataitem_handle = 'dataitem_'+str(dataitem.id)
				if dataitem_handle in key:
					answer_item_value[key.replace(dataitem_handle,'')] = request.POST[key]

			new_answer_item = AnswerItem(answer = new_answer,dataitem = dataitem, value = answer_item_value)
			new_answer_item.save()
	
		if len(taskinstance.answers) >= taskinstance.task.min_answers_per_item:
			taskinstance.status = 'FN'
			taskinstance.save()

		logEvent(request, 'execution_completed',taskinstance.task.id, taskinstance.id)
	else:
		logEvent(request, 'execution_completed_withmistake_notsaved',taskinstance.task.id, taskinstance.id)
	return redirect(reverse('cafe-taskinstance-assign', kwargs={'task_id': taskinstance.task.id})+'?completed_previous=1')


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


def instancesAvailableExist(task, user, instance_id = 0):
	answers = Answer.objects.filter(executor = user, taskinstance__task = task).values('taskinstance')

	instances = TaskInstance.objects.filter(task = task, status = 'ST', pk__gt = instance_id).exclude(pk__in = answers)
	if instances.count()>0:
		return instances
	else:
		return False