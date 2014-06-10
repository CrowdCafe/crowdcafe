#!/usr/bin/env python
#coding: utf8 
from django.db import models
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from datetime import datetime 
import jsonfield
from decimal import Decimal
from datetime import  timedelta
from account.models import AccountTransaction
from django.conf import settings

from django.db.models import Sum

import requests
import json
import urllib2

STATUS_CHOISE = (('PR', 'In process'), ('ST', 'Published'), ('FN', 'Finished'), ('NP', 'Not published'), ('NR','Not ready'),('DL', 'Deleted'))

def getPlatformOwner():
    return User.objects.filter(pk = settings.BUSINESS['platform_owner_id']).get()
    
def calculateCommission(amount):
    return amount * settings.BUSINESS['platform_commission']

class Job(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=255, default='New task')
    description = models.CharField(max_length=1024, default='***')

    category = models.CharField(max_length=2, default='CF', blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOISE, default='NP')

    date_created = models.DateTimeField(auto_now_add=True, auto_now=False) 
    date_deadline = models.DateTimeField(default=lambda: (datetime.now() + timedelta(days=7)), auto_now_add=False)

    webhook_url = models.URLField(null = True, blank = True)
    template_url = models.URLField(null = True, blank = True)
    template_html = models.TextField(null = True, blank = True)
    
    def category_icon(self):
        return settings.TASK_CATEGORIES[self.category]['icon']
    def refresh_template(self):
        try:
            self.template_html = urllib2.urlopen(self.template_url).read()
            self.save()
            return True
        except:
            return False
    @property
    def amount_tasks(self):
        return Task.objects.filter(job = self, status = 'ST').count()
    @property
    def category_details(self):
        return settings.TASK_CATEGORIES[self.category]

class Attachment(models.Model):
    job = models.ForeignKey(Job, null = True, blank = True)
    file = models.FileField(upload_to='attachments', blank = True)

class DataItem(models.Model):
    job = models.ForeignKey(Job)
    value = jsonfield.JSONField()
    gold = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOISE, default = 'NR')
    @property
    def tasks(self):
        return Task.objects.filter(dataitems = self).all()
    @property
    def answeritems(self):
        return AnswerItem.objects.filter(dataitem = self).all()
    def refreshStatus(self):
        if not self.gold:
            print len(self.answeritems)
            if len(self.answeritems) >= self.job.qualitycontrol.min_answers_per_item:
                self.status = 'FN'
                self.save()
                print 'status changed'
    def __unicode__(self):
        return str(self.id)

class Task(models.Model):
    job = models.ForeignKey(Job)
    status = models.CharField(max_length=2, choices=STATUS_CHOISE, default='ST')
    dataitems = models.ManyToManyField(DataItem, blank = True, null = True)
    @property 
    def items(self):
        return self.dataitems.all()
    @property
    def answers(self):
        return Answer.objects.filter(task = self).all()

class Answer(models.Model):
    task = models.ForeignKey(Task)
    executor = models.ForeignKey(User, blank = True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOISE, default='ST', blank=True)

    def __unicode__(self):
        return str(self.id)
    @property
    def score(self):
        score = 0.0
        for answeritem in self.answeritems:
            score+=answeritem.score
        return score
    
    @property
    def answeritems(self):
        return AnswerItem.objects.filter(answer = self).all()
    def webhook(self):
        if self.task.job.webhook_url:
            print 'webhook started'
            i=0
            data = {}
            for answeritem in self.answeritem_set.all():
                data['data['+str(i)+']'] = json.dumps(answeritem.value)
                i+=1
            data['length']=i
            try:
                r = requests.post(self.task.job.webhook_url, data = (data))
                return True
            except:
                return False
        return False
    def save(self, *args, **kwargs):
        #if answer is new, task reward is greater than 0 and the worker and the requestor are different people
        if self.pk is None and self.task.job.category_details['cost']>0 and self.executor.profile.account != self.task.job.owner.profile.account:

            # Worker gets money from Requestor
            transaction = AccountTransaction(currency = 'VM', to_account = self.executor.profile.account, from_account = self.task.job.owner.profile.account, amount = self.task.job.category_details['cost'], description = 'answer for t.i. ['+str(self.task.id)+']')
            transaction.save()

            # Platform gets comission from Requestor
            commission = AccountTransaction(currency = 'VM', to_account = getPlatformOwner().profile.account, from_account = self.task.job.owner.profile.account, amount = calculateCommission(transaction.amount), description = 'comission for answer for t.i. ['+str(self.task.id)+']')
            commission.save()
        super(Answer, self).save(*args, **kwargs)

class AnswerItem(models.Model):
    answer = models.ForeignKey(Answer, blank = True)
    dataitem = models.ForeignKey(DataItem, blank = True)
    value = jsonfield.JSONField()
    score = models.FloatField(default = 0.0, null = True, blank = True)
    def __unicode__(self):
        return str(self.id)
    @property
    def question(self):
        try:
            return self.dataitem.value
        except:
            return ''
    @property
    def worker_id(self):
        try:
            return self.answer.executor.id
        except:
            return 0
    @property
    def date_created(self):
        try:
            return self.answer.date_created
        except:
            return ''
    @property
    def task_id(self):
        try:
            return self.answer.task.id
        except:
            return 0
    @property
    def task_status(self):
        try:
            return self.answer.task.status
        except:
            return ''

