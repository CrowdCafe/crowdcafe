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

from account.models import Account, FundTransfer
from math import *
from utility.general import getSample, getSubset
from django.db.models.signals import post_save
from django.db.models import Q
import random
import numpy
import logging

log = logging.getLogger(__name__)

#TODO - Need to find a way to combine this and TASK_CATEGORIES from settings.
from utility.utils2 import notifyMoneyAdmin

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

    def fundsAreSufficientToCoverAssignment(self, subset):
        units_count = len(subset)
        # if account is admins or if the balance with some allowed debt (from BUSINESS in settings) is above potential expenses
        if self.app.account.id == settings.BUSINESS['platform_owner_account_id'] or (self.app.account.balance+Decimal(settings.BUSINESS['allow_debt']) >= Decimal(units_count*self.price) + Decimal(units_count*settings.BUSINESS['platform_commission'])):
            return True
        else:
            account = self.app.account
            notifyMoneyAdmin(account,2)
            return False
    
    def refreshUserInterface(self):
        try:
            self.userinterface_html = urllib2.urlopen(self.userinterface_url).read()
            self.save()
            return True
        except:
            return False
    def assignUnits(self,worker,regular_units_only = False):
        units_completed_by_worker = Judgement.objects.filter(unit__job = self, worker = worker).values('unit')
        # get units which are published and do not have any judgements provided by the worker
        units = Unit.objects.filter(job = self, status = 'NC', published = True).exclude(pk__in = units_completed_by_worker)
        # set of available gold units
        units_gold = [x for x in units if x.gold]
        # set of available regular units
        units_regular = [x for x in units if not x.gold]
        # current workers score in this job
        evaluations_negative = self.qualitycontrol.evaluated_amount(worker, False)

        if len(units_regular) > 0 and evaluations_negative <= self.qualitycontrol.incorrect_allowed:
            # if it is a gold creation task
            if regular_units_only and worker in self.app.account.users.all():
                subset = getSubset(units_regular,self.units_per_page)
            else:
                # if gold is required and exists
                gold_amount_to_inject = min(self.qualitycontrol.amountOfGoldToInject(worker),len(units_gold))

                subset_gold = getSubset(units_gold,gold_amount_to_inject)
                subset_regular = getSubset(units_regular,abs(self.units_per_page - gold_amount_to_inject))
                subset = subset_gold + subset_regular
                # if there is no enough money on the account 
                if not self.fundsAreSufficientToCoverAssignment(subset):
                    subset = False
            return subset
        else:
            return False
    # IMPORTANT: i've implemented this to have the price set
    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = settings.TASK_CATEGORIES[self.category]['cost']
        super(Job, self).save(*args, **kwargs)
    # estimated amount of tasks left available for a specific user
    @property
    def estimatedTasksLeft(self):
        # get the integer number of groups of units 
        return int(ceil(Unit.objects.filter(status = 'NC', published = True, job = self).count() / self.units_per_page))

class QualityControl(models.Model):
    job = models.OneToOneField(Job)
    min_judgements_per_unit = models.IntegerField(default=1)
    max_units_per_worker = models.IntegerField(default=100)  # Some limitation of amount of units single worker can complete ideally in percentage
    gold_min = models.IntegerField(default=0, null=True)
    gold_max = models.IntegerField(default=0, null=True)
    incorrect_allowed = models.IntegerField(default=0, null=True)
    qualitycontrol_url = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return str(self.id)
    def score(self, worker):
        return Judgement.objects.filter(unit__job=self.job, worker = worker).aggregate(Sum('score'))['score__sum']
    def evaluated_amount(self, worker, correct = True):
        evaluated_queryset = Judgement.objects.filter(unit__job=self.job, worker = worker)
        if correct:
            evaluated_queryset = evaluated_queryset.filter(score__gt = 0)
        else:
            evaluated_queryset = evaluated_queryset.filter(score__lt = 0)
            
        evaluated = evaluated_queryset.aggregate(Sum('score'))['score__sum']
        if evaluated:
            evaluated = abs(evaluated)
        else:
            evaluated = 0
        return evaluated
    
    def getProbabilityToInjectGold(self,worker):
        #TODO #EMAIL do we need this 1.0 in the beginning if we want to get float value?
        return 1.0*(1+self.evaluated_amount(worker, False))/(1+self.evaluated_amount(worker, True)+self.evaluated_amount(worker, False))
    def amountOfGoldToInject(self,worker):
        gold_units = [[0, 1][numpy.random.random() < self.getProbabilityToInjectGold(worker)] for _ in range(self.job.units_per_page)]
        return sum(gold_units)

@receiver(post_save, sender=Job)
def initJob(sender, **kwargs):
    job = kwargs['instance']
    qualitycontrol, created = QualityControl.objects.get_or_create(job = job)

# ====================================================
# DATA UNITS RELATED CLASSES

UNIT_STATUS_CHOISES = (('NC', 'Not completed'), ('CD', 'Completed'))

class Unit(models.Model):
    job = models.ForeignKey(Job)
    input_data = jsonfield.JSONField()
    status = models.CharField(max_length=2, choices=UNIT_STATUS_CHOISES, default='NC')
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    deleted = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default = True) 

    def __unicode__(self):
        return str(self.id)
    @property
    def gold(self):
        # if this unit has any judgements marked as gold
        return Judgement.objects.filter(unit = self, gold = True).count()>0
    @property
    def judgements(self):
        return Judgement.objects.filter(unit = self)
    
    def updateStatus(self):
        if self.judgements.count() >= self.job.qualitycontrol.min_judgements_per_unit and not self.gold:
            self.status = 'CD'
            self.save()
        return self.status
    def save(self, *args, **kwargs):
        log.debug('unit '+str(self.pk)+' was saved, its status = '+str(self.status))
        # if the job is published, there are no 

        # if this unit is not new
        if self.pk is not None:
            orig = Unit.objects.get(pk=self.pk)
            # if the status of this unit is "Completed" and before it was different
            if orig.status != self.status and self.status == 'CD':
                published_units = Unit.objects.filter(job = self.job, published = True)
                # if all the published units completed notify admin of the account 
                #TODO - as we update status via API - admin might receive multiple emails even when not all judgements are fully completed.
                if self.job.status == 'PB' and published_units.filter(status = 'NC').count() == 0 and published_units.filter(status = 'CD').count() > 0:
                    notifyMoneyAdmin(self.job.app.account,3)
        
        super(Unit, self).save(*args, **kwargs)
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
        if self.pk is None and self.unit.job.price>0 and self.score >= 0:

            # Worker gets money from Requestor
            fundtransfer = FundTransfer(to_account = self.worker.profile.personalAccount, from_account = self.unit.job.app.account, amount = self.unit.job.price, description = 'judgement for unit ['+str(self.unit.id)+']')
            fundtransfer.save()
            
            # Platform gets comission from Requestor
            platform_owner_account = Account.objects.get(pk = settings.BUSINESS['platform_owner_account_id'])
            commission = FundTransfer(to_account = platform_owner_account, from_account = self.unit.job.app.account, amount = Decimal(settings.BUSINESS['platform_commission'])*fundtransfer.amount, description = 'commission for judgement for unit ['+str(self.unit.id)+']')
            commission.save()
        super(Judgement, self).save(*args, **kwargs)


class Notification(models.Model):
    job = models.ForeignKey(Job, null = True, blank = True)
    last = models.DateField(auto_now=True)


class Attachment(models.Model):
    job = models.ForeignKey(Job, null = True, blank = True)
    source_file = models.FileField(upload_to='attachments')