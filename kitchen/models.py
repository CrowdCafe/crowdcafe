#!/usr/bin/env python
#coding: utf8 
from django.db import models
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from datetime import datetime 
from decimal import Decimal
from datetime import  timedelta

#from pyuploadcare.dj import FileField

STATUS_CHOISE = (('PR', 'In process'), ('ST', 'Stopped'), ('FN', 'Finished'), ('DL', 'Deleted'),)
CATEGORY_CHOISE = (('CF', 'Caffè'), ('CP', 'Cappuccino'), ('WN', 'Wine'),)
TEMPLATE_CHOISE = (('PC', 'Pair comparison'), ('SA', 'Sentiment Analysis'), ('SS', 'Subset selection'),)

class Task(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=200, default='New task')
    description = models.CharField(max_length=1000, default='***')

    category = models.CharField(max_length=2, choices=CATEGORY_CHOISE, default='CF', blank=True)
    template = models.CharField(max_length=2, choices=TEMPLATE_CHOISE, default='PR', blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOISE, default='ST', blank=True)

    dataset_file = models.FileField(upload_to='datasets',blank = True)
    date_created = models.TimeField(auto_now_add=True, auto_now=False) 
    date_deadline = models.DateTimeField(default=lambda: (datetime.now() + timedelta(days=7)), auto_now_add=False)