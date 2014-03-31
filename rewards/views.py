from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.conf import settings
import uuid
from models import Vendor, Reward, RewardInstance

@login_required
def VendorNew(request):
	
	return render_to_response('rewards/vendor.html', context_instance=RequestContext(request))

@login_required
def VendorSave(request):
	new_vendor = Vendor(
			owner = request.user,

			title = request.POST['vendor_title'],
			description = request.POST['vendor_description'],
			image_url = request.POST['vendor_image_url'],
			website_url = request.POST['vendor_website_url'],
			address = request.POST['vendor_address']
			)
	new_vendor.save()
	return redirect('rewards-home')

@login_required
def RewardNew(request,vendor_id):
	vendor = get_object_or_404(Vendor, pk = vendor_id)
	return render_to_response('rewards/reward.html', {'vendor':vendor} ,  context_instance=RequestContext(request))

@login_required
def RewardSave(request, vendor_id):
	vendor = get_object_or_404(Vendor, pk = vendor_id)
	new_reward = Reward(
			owner = request.user,
			vendor = vendor,
			title = request.POST['reward_title'],
			description = request.POST['reward_description'],
			image_url = request.POST['reward_image_url'],
			website_url = request.POST['reward_website_url'],
			cost = float(request.POST['reward_cost'])
			)
	new_reward.save()
	return redirect('rewards-home')

@login_required
def RewardInstances(request, reward_id):
	reward = get_object_or_404(Reward, pk = reward_id)
	instances = RewardInstance.objects.filter(reward = reward).all()
	return render_to_response('rewards/instances.html', {'reward':reward,'instances':instances}, context_instance=RequestContext(request))

@login_required
def RewardInstancesGenerate(request, reward_id):
	amount = 5
	reward = get_object_or_404(Reward,pk = reward_id)
	for i in range(amount):
		instance = RewardInstance(reward= reward)
		instance.save()
	return redirect(reverse('rewards-vendor-reward-instances', kwargs={'reward_id': reward_id}))
def Home(request):
	vendors = Vendor.objects.all()

	return render_to_response('rewards/home.html', {'vendors':vendors}, context_instance=RequestContext(request))

