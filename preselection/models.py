from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from kitchen.models import Job

#=========================================================================
# PRESELECTION
#=========================================================================

TYPE_CHOISE = (('WO', 'worked on'), ('NW', 'did not work on'))

class Preselection(models.Model):
	job = models.ForeignKey(Job)
	related_job = models.ForeignKey(Job, related_name = 'related_task')
	rule_type = models.CharField(max_length = 2, choices = TYPE_CHOISE, default='WO')
    
