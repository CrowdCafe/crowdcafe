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


STATUS_CHOISE = (('PR', 'In process'), ('ST', 'Stopped'), ('FN', 'Finished'), ('DL', 'Deleted'), ('NP', 'Not published'))
CATEGORY_CHOISE = (('CF', 'Caffè'), ('CP', 'Cappuccino'), ('WN', 'Wine'),)
TEMPLATE_CHOISE = (('SF', 'Single form'), ('LT', 'List'), ('TL', 'Tiles'),)

def getPlatformOwner():
    return User.objects.filter(pk = settings.BUSINESS['platform_owner_id']).get()
def calculateCommission(amount):
    return amount * settings.BUSINESS['platform_commission']

class Task(models.Model):
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

    dataitems_per_instance = models.IntegerField(default = 5)
    min_answers_per_item = models.IntegerField(default = 1)
    min_confidence = models.IntegerField(default = 50)

    template_url = models.URLField(null = True, blank = True)
    template_html = models.TextField(null = True, blank = True)
    
    @property
    def amount_instances(self):
        return TaskInstance.objects.filter(task = self, status = 'ST').count()
    @property
    def category_details(self):
        return settings.TASK_CATEGORIES[self.category]

class TaskInstance(models.Model):
    task = models.ForeignKey(Task)
    status = models.CharField(max_length=2, choices=STATUS_CHOISE, default='ST')
    @property
    def dataitems(self):
        return DataItem.objects.filter(taskinstance = self).all()
    @property
    def answers(self):
        return Answer.objects.filter(taskinstance = self).all()

class DataItem(models.Model):
    taskinstance = models.ForeignKey(TaskInstance)
    value = jsonfield.JSONField()
    @property
    def answeritems(self):
        return AnswerItem.objects.filter(dataitem = self).all()
    def __unicode__(self):
        return str(self.id)

class Answer(models.Model):
    taskinstance = models.ForeignKey(TaskInstance)
    executor = models.ForeignKey(User, blank = True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOISE, default='ST', blank=True)

    def __unicode__(self):
        return str(self.id)
    @property
    def answeritems(self):
        return AnswerItem.objects.filter(answer = self).all()


    def save(self, *args, **kwargs):
        if self.pk is None:

            # Worker gets money from Requestor
            transaction = AccountTransaction(currency = 'VM', to_account = self.executor.profile.account, from_account = self.taskinstance.task.owner.profile.account, amount = self.taskinstance.task.category_details['cost'], description = 'answer for t.i. ['+str(self.taskinstance.id)+']')
            transaction.save()

            # Platform gets comission from Requestor
            commission = AccountTransaction(currency = 'VM', to_account = getPlatformOwner().profile.account, from_account = self.taskinstance.task.owner.profile.account, amount = calculateCommission(transaction.amount), description = 'comission for answer for t.i. ['+str(self.taskinstance.id)+']')
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
        return self.dataitem.value
    @property
    def worker_id(self):
        return self.answer.executor.id

