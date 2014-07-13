from django.db import models

from account.models import Account, FundTransfer
from django.contrib.auth.models import User
import string
import random
from random import randint

REWARD_STATUSES = (('NV', 'Not visible'), ('AV', 'Available'), ('AC', 'Activated'), ('UD', 'Used'))

def id_generator(size=4, chars=string.ascii_lowercase + string.digits):
    code = ''.join(random.choice(chars) for x in range(size))
    print(code)
    return code
def generateRewardCode():
	# 1234-5678-9012-3456
	code = ''
	for i in range(2):
		if code!='':
			code+='-'
		code+=str(randint(1000, 9999))
	return code

class Vendor(models.Model):
	account = models.ForeignKey(Account)

	title = models.CharField(max_length=255, default='New vendor')
	description = models.CharField(max_length=1024, null=True, blank=True)
	image_url = models.URLField(null=True, blank=True)
	website_url = models.URLField(null=True, blank=True)
	address = models.CharField(max_length=1024, null=True, blank=True)
	creator = models.ForeignKey(User)
	@property
	def rewards(self):
		return Reward.objects.filter(vendor = self).all()

class Reward(models.Model):
	vendor = models.ForeignKey(Vendor)

	title = models.CharField(max_length=255, default='New reward')
	description = models.CharField(max_length=1024, null=True, blank=True)
	image_url = models.URLField(null=True, blank=True)
	website_url = models.URLField(null=True, blank=True)
	creator = models.ForeignKey(User)
	
	cost_for_worker = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	cost_for_platform = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

	def generateCoupons(self, amount):
		for i in range(amount):
			coupon = Coupon(self = reward)
			coupon.save()
		return True
	@property
	def amount_available(self):
		return Coupon.objects.filter(reward = self, status = 'AV').count()

class Coupon(models.Model):
	reward = models.ForeignKey(Reward)
	status = models.CharField(max_length=2, choices=REWARD_STATUSES, default='NV')	
	account = models.ForeignKey(Account, null=True, blank=True)

	code = models.CharField(max_length=32,default=lambda: generateRewardCode())

	date_created = models.DateTimeField(auto_now_add=True, auto_now=False) 
	date_updated = models.DateTimeField(auto_now_add=True, auto_now=True) 