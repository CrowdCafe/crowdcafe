from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from kitchen.models import Job

#=========================================================================
# QUALITY CONTROL
#=========================================================================

class QualityControl(models.Model):
    job = models.OneToOneField(Job)
    min_confidence = models.FloatField(default = 50, null = True)
    gold_min = models.IntegerField(default = 0, null = True)
    gold_max = models.IntegerField(default = 0, null = True)
    score_min = models.FloatField(default = 0, null = True)
    dataitems_per_task = models.IntegerField(default = 5)
    min_answers_per_item = models.IntegerField(default = 1)

