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

import requests
import json
import urllib

STATUS_CHOISE = (('PR', 'In process'), ('ST', 'Stopped'), ('FN', 'Finished'), ('DL', 'Deleted'), ('NP', 'Not published'), ('NR','Not ready'))
CATEGORY_CHOISE = (('CF', 'Caffè'), ('CP', 'Cappuccino'), ('WN', 'Wine'),)
TEMPLATE_CHOISE = (('SF', 'Single form'), ('LT', 'List'), ('TL', 'Tiles'),)

def getPlatformOwner():
    return User.objects.filter(pk = settings.BUSINESS['platform_owner_id']).get()
def calculateCommission(amount):
    return amount * settings.BUSINESS['platform_commission']

class Job(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=255, default='New task')
    description = models.CharField(max_length=1024, default='***')

    category = models.CharField(max_length=2, choices=CATEGORY_CHOISE, default='CF', blank=True)
    template = models.CharField(max_length=2, choices=TEMPLATE_CHOISE, default='PR', blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOISE, default='NP')

    dataset_file = models.FileField(upload_to='datasets',blank = True)
    options_file = models.FileField(upload_to='options',blank = True)

    date_created = models.DateTimeField(auto_now_add=True, auto_now=False) 
    date_deadline = models.DateTimeField(default=lambda: (datetime.now() + timedelta(days=7)), auto_now_add=False)

    dataitems_per_task = models.IntegerField(default = 5)
    min_answers_per_item = models.IntegerField(default = 1)
    min_confidence = models.IntegerField(default = 50)
    webhook_url = models.URLField(null = True, blank = True)
    template_url = models.URLField(null = True, blank = True)
    template_html = models.TextField(null = True, blank = True)
    
    @property
    def amount_tasks(self):
        return Task.objects.filter(job = self, status = 'ST').count()
    @property
    def category_details(self):
        return settings.TASK_CATEGORIES[self.category]

class DataItem(models.Model):
    job = models.ForeignKey(Job)
    value = jsonfield.JSONField()
    @property
    def tasks(self):
        return Task.objects.filter(dataitems = self).all()
    @property
    def answeritems(self):
        return AnswerItem.objects.filter(dataitem = self).all()
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
    def answeritems(self):
        return AnswerItem.objects.filter(answer = self).all()
    def webhook(self):
        print 'webhook started'
        if self.task.job.webhook_url:
            i=0
            data = {}
            for answeritem in self.answeritem_set.all():
                data['data['+str(i)+']'] = json.dumps(answeritem.value)
                i+=1
            data['length']=i
            print data
            r = requests.post(self.task.job.webhook_url, data = (data))
            print r.text
            '''try:
                r = requests.post(self.task.job.webhook_url, data=json.dumps(data))
                print r.json()
            except: 
                print 'we experienced a problem'
                return False
            '''
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
    '''
    @property
    def dataitem_id(self):
        try:
            return self.dataitem.id
        except:
            return 0
    '''
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


