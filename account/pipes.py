#from social_auth.backends.facebook import FacebookBackend
from models import Profile, Account
import time
import logging


def get_user_addinfo(backend, details, response, social_user, uid,\
                    user, *args, **kwargs):
    log = logging.getLogger(__name__)
    log.debug('here we are')
    #load profile, defaults when creation empty
    #it returns a touple, profile is the object, created is the boolean if it's created or exists
    profile, created = Profile.objects.get_or_create(user=user)

    if created:
        log.debug('created')
    else:
        log.debug('name: %s' %(user.username))
    #if facebook then steal data
    profile.save()
    account = Account.objects.get_or_create(profile=profile)