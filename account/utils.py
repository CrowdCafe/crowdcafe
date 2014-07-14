from django.db import models
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from datetime import datetime 
from models import Profile, Account, Membership
from django.conf import settings

def getPlatformOwner():
    return Account.objects.filter(pk = settings.BUSINESS['platform_owner_account_id']).get()
    
def calculateCommission(amount):
    return amount * settings.BUSINESS['platform_commission']