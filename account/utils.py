from django.db import models
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from datetime import datetime 
from models import Profile, Account, Membership
from django.conf import settings

def initUser(user):
	# create a profile for using its properties 
	profile, created = Profile.objects.get_or_create(user=user)
	
	# create a personal account
	account, created = Account.objects.get_or_create(creator = user, personal = True, title = 'personal account')

	# add current user to this account with Admin permission
	membership, created = Membership.objects.get_or_create(user = user, permission = 'AN', account = account)

def getPlatformOwner():
    return Account.objects.filter(pk = settings.BUSINESS['platform_owner_account_id']).get()
    
def calculateCommission(amount):
    return amount * settings.BUSINESS['platform_commission']