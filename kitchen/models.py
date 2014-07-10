from datetime import datetime
from decimal import Decimal
from datetime import timedelta
import json
import urllib2
import os
import binascii

from django.db import models
from social_auth.models import UserSocialAuth
import jsonfield
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
import requests

from rest_framework.authtoken.models import Token

from CrowdCafe.settings_common import TASK_CATEGORIES

from account.models import Account, FundTransfer
from math import *

#TODO - Need to find a way to combine this and TASK_CATEGORIES from settings.
TASK_CATEGORY_CHOICES = (
    ('EP','Espresso',),
    ('CP','Cappuccino'),
    ('WN','Wine'),  
    )

DEVICE_CHOISES = (('MO', 'Mobile only'), ('DO', 'Desktop only'), ('AD', 'Any device'))
# ====================================================
# JOBS RELATED CLASSES:

class App(models.Model):
    account = models.ForeignKey(Account)
    creator = models.ForeignKey(User)  # the one created the app
    token = models.CharField(max_length=40, blank=True)
    title = models.CharField(max_length=100)
    deleted = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = binascii.hexlify(os.urandom(20))
        return super(App, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.id)
        #def __unicode__(self):
        #    return '' + str(self.owner.username) + ' - ' + str(self.name) # TODO this should be redone according to accounts approach


JOB_STATUS_CHOISES = (('NP', 'Not published'), ('PB', 'Published'))


class Job(models.Model):
    # general
    app = models.ForeignKey(App)
    creator = models.ForeignKey(User)  # the one created the job
    title = models.CharField(max_length=255, default='New job')
    description = models.TextField()
    category = models.CharField(max_length=2, choices=TASK_CATEGORY_CHOICES)

    # settings
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.03) # reward worker gets per unit
    units_per_page = models.IntegerField(default=5)
    device_type = models.CharField(max_length=2, choices=DEVICE_CHOISES, default='AD')
    
    # api+notification
    judgements_webhook_url = models.URLField(null=True, blank=True) # every time a worker submits judgements, POST is sent on this url with judgements data

    # userinterface
    userinterface_url = models.URLField(null=True, blank=True) # if this is filled - html is taken from here to set userinterface_html
    userinterface_html = models.TextField(null=True, blank=True)
    # make sure we do not have anly volnurabilities in userinterface_html
    
    # other
    status = models.CharField(max_length=2, choices=JOB_STATUS_CHOISES, default='NP')
    deleted = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __unicode__(self):
        return str(self.id)

    def refreshUserInterface(self):
        try:
            self.userinterface_html = urllib2.urlopen(self.userinterface_url).read()
            self.save()
            return True
        except:
            return False

    # IMPORTANT: i've implemented this to have the price set
    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = TASK_CATEGORIES[self.category]['cost']
        super(Job, self).save(*args, **kwargs)
    # estimated amount of tasks left available for a specific user
    @property
    def estimatedTasksLeft(self):
        # get the integer number of groups of units 
        return int(ceil(Unit.objects.filter(status = 'NC', published = True, job = self).count() / self.units_per_page))

class QualityControl(models.Model):
    job = models.OneToOneField(Job)
    min_judgements_per_unit = models.IntegerField(default=1)
    max_units_per_worker = models.IntegerField(default=100)  # Some limitation of amount of units single worker can complete
    gold_min = models.IntegerField(default=0, null=True)
    gold_max = models.IntegerField(default=0, null=True)
    score_min = models.IntegerField(default=0, null=True)
    qualitycontrol_url = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return str(self.id)

# ====================================================
# DATA UNITS RELATED CLASSES

UNIT_STATUS_CHOISES = (('NC', 'Not completed'), ('CD', 'Completed'))

class Unit(models.Model):
    job = models.ForeignKey(Job)
    input_data = jsonfield.JSONField()
    status = models.CharField(max_length=2, choices=UNIT_STATUS_CHOISES, default='NC')
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    deleted = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default = False) 

    def __unicode__(self):
        return str(self.id)
    @property
    def judgements(self):
        return Judgement.objects.filter(unit = self)
    
    def updateStatus(self):
        if self.judgements.count() >= self.job.qualitycontrol.min_judgements_per_unit:
            self.status = 'CD'
            self.save()
        return self.status

    def saveJudgement(self, postdata, worker):
        judgement_output_data = {}
        for key in postdata:
            # only if a POST data has a key with dataunit_handle - it will be saved (otherwise we can not find a connection to a specific unit)
            dataunit_handle = 'dataitem_'+str(self.id)
            if dataunit_handle in key:
                judgement_output_data[key.replace(dataunit_handle,'')] = postdata[key]
                #TODO - check gold data
        #TODO external quality control
        judgement = Judgement(unit = self, output_data =judgement_output_data, worker = worker)
        judgement.save()
        
        self.updateStatus()
        
        return judgement

# ====================================================
# JUDGEMENTS RELATED CLASSES

class Judgement(models.Model):
    unit = models.ForeignKey(Unit, blank=True)
    output_data = jsonfield.JSONField(blank=True)
    score = models.FloatField(default=0.0, null=True, blank=True)
    worker = models.ForeignKey(User, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    # Don't see a reason to have extra class for GoldJudgements, as we won't have any extra fields in it
    gold = models.BooleanField(default = False) 

    def __unicode__(self):
        return str(self.id)
    def save(self, *args, **kwargs):
        #if answer is new, task reward is greater than 0 and the worker and the requestor are different people
        if self.pk is None and self.unit.job.price>0:

            # Worker gets money from Requestor
            fundtransfer = FundTransfer(currency = 'VM', to_account = self.worker.profile.personalAccount, from_account = self.unit.job.app.account, amount = self.unit.job.price, description = 'answer for t.i. ['+str(self.id)+']')
            fundtransfer.save()

            # Platform gets comission from Requestor
            # commission = AccountTransaction(currency = 'VM', to_account = getPlatformOwner().profile.account, from_account = self.task.job.owner.profile.account, amount = calculateCommission(transaction.amount), description = 'comission for answer for t.i. ['+str(self.task.id)+']')
            # commission.save()
        super(Judgement, self).save(*args, **kwargs)
