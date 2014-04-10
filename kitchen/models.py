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


STATUS_CHOISE = (('PR', 'In process'), ('ST', 'Stopped'), ('FN', 'Finished'), ('DL', 'Deleted'),)
CATEGORY_CHOISE = (('CF', 'Caffè'), ('CP', 'Cappuccino'), ('WN', 'Wine'),)
TEMPLATE_CHOISE = (('SF', 'Single form'), ('LT', 'List'), ('TL', 'Tiles'),)

class Task(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=255, default='New task')
    description = models.CharField(max_length=1024, default='***')

    category = models.CharField(max_length=2, choices=CATEGORY_CHOISE, default='CF', blank=True)
    template = models.CharField(max_length=2, choices=TEMPLATE_CHOISE, default='PR', blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOISE, default='ST')

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
        return TaskInstance.objects.filter(task = self).count()

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
            transaction = AccountTransaction(owner = self.executor.profile.account,amount = 0.03, type = 'EG', description = 'task_instance ['+str(self.taskinstance.id)+'] completed')
            transaction.save()
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

