from models import Profile, Account
import time
import logging

from utils import initUser

def get_user_addinfo(backend, details, response, social_user, uid,\
                    user, *args, **kwargs):
    log = logging.getLogger(__name__)
    log.debug('here we are')
    #load profile, defaults when creation empty
    #it returns a touple, profile is the object, created is the boolean if it's created or exists
    initUser(user)