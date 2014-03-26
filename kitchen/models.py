#!/usr/bin/env python
#coding: utf8 
from django.db import models
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from datetime import datetime 
import jsonfield
from decimal import Decimal
from datetime import  timedelta



STATUS_CHOISE = (('PR', 'In process'), ('ST', 'Stopped'), ('FN', 'Finished'), ('DL', 'Deleted'),)
CATEGORY_CHOISE = (('CF', 'Caffè'), ('CP', 'Cappuccino'), ('WN', 'Wine'),)
TEMPLATE_CHOISE = (('PC', 'Pair comparison'), ('SR', 'Swiping rows'), ('SS', 'Subset selection'),)

class Task(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=200, default='New task')
    description = models.CharField(max_length=1000, default='***')

    category = models.CharField(max_length=2, choices=CATEGORY_CHOISE, default='CF', blank=True)
    template = models.CharField(max_length=2, choices=TEMPLATE_CHOISE, default='PR', blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOISE, default='ST', blank=True)

    dataset_file = models.FileField(upload_to='datasets',blank = True)
    options_file = models.FileField(upload_to='options',blank = True)

    date_created = models.DateTimeField(auto_now_add=True, auto_now=False) 
    date_deadline = models.DateTimeField(default=lambda: (datetime.now() + timedelta(days=7)), auto_now_add=False)

    dataitems_per_instance = models.IntegerField(default = 5)
    min_answers_per_item = models.IntegerField(default = 1)
    min_confidence = models.IntegerField(default = 50)

class TaskInstance(models.Model):
    task = models.ForeignKey(Task)
    @property
    def dataitems(self):
        return DataItem.objects.filter(taskinstance = self).all()

class DataItem(models.Model):
    taskinstance = models.ForeignKey(TaskInstance)
    value = jsonfield.JSONField()
    def __unicode__(self):
        return str(self.id)

class Answer(models.Model):
    executor = models.ForeignKey(User, blank = True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOISE, default='ST', blank=True)

    def __unicode__(self):
        return str(self.id)

class AnswerItem(models.Model):
    answer = models.ForeignKey(Answer, blank = True)
    dataitem = models.ForeignKey(DataItem, blank = True)
    value = jsonfield.JSONField()
    def __unicode__(self):
        return str(self.id)
