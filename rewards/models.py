from django.db import models

from django.contrib.auth.models import User
from account.models import AccountTransaction
import string
import random

REWARD_STATUSES = (('NA', 'Not active'), ('AC', 'Active'), ('PS', 'Purchased'))

def id_generator(size=4, chars=string.ascii_lowercase + string.digits):
    code = ''.join(random.choice(chars) for x in range(size))
    print(code)
    return code

class Vendor(models.Model):
	title = models.CharField(max_length=255, default='New vendor')
	description = models.CharField(max_length=1024, null=True, blank=True)
	image_url = models.URLField(null=True, blank=True)
	website_url = models.URLField(null=True, blank=True)
	
	owner = models.ForeignKey(User)
	address = models.CharField(max_length=1024, null=True, blank=True)
	@property
	def rewards(self):
		return Reward.objects.filter(vendor = self).all()
class Reward(models.Model):
	vendor = models.ForeignKey(Vendor)

	title = models.CharField(max_length=255, default='New reward')
	description = models.CharField(max_length=1024, null=True, blank=True)
	image_url = models.URLField(null=True, blank=True)
	website_url = models.URLField(null=True, blank=True)
	
	owner = models.ForeignKey(User)
	cost = models.FloatField()

class RewardInstance(models.Model):
	reward = models.ForeignKey(Reward)
	status = models.CharField(max_length=2, choices=REWARD_STATUSES, default='NA')
	worker = models.ForeignKey(User, null=True, blank=True)
	transaction = models.ForeignKey(AccountTransaction, null=True, blank=True)
	
	index = models.IntegerField(null=True, blank=True)
	code = models.CharField(max_length=32,default=lambda: id_generator()+'-'+id_generator()+'-'+id_generator()+'-'+id_generator())

	date_created = models.DateTimeField(auto_now_add=True, auto_now=False) 
	date_updated = models.DateTimeField(auto_now_add=True, auto_now=True) 