from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from kitchen.models import Job, Answer, AnswerItem, DataItem

#=========================================================================
# QUALITY CONTROL
#=========================================================================
DEVICES_ALLOWED = ((0,'Any device'),(1,'Mobile'),(2,'Desktop'))

class QualityControl(models.Model):
    job = models.OneToOneField(Job)
    min_confidence = models.FloatField(default = 50, null = True)
    gold_min = models.IntegerField(default = 0, null = True)
    gold_max = models.IntegerField(default = 0, null = True)
    score_min = models.FloatField(default = 0, null = True)
    dataitems_per_task = models.IntegerField(default = 5)
    min_answers_per_item = models.IntegerField(default = 1)
    max_dataitems_per_worker = models.FloatField(default = 100)
    device_type = models.IntegerField(default = 0, null = True)
    qualitycontrol_url = models.URLField(null = True, blank = True)

    def allowed_to_work_more(self, user):
        
        performed_items = AnswerItem.objects.filter(answer__task__job = self.job, dataitem__gold = False, answer__executor = user).count()
        all_items = DataItem.objects.filter(job = self.job, gold = False).count()

        score = self.score(user)
        if (all_items >0 and (performed_items/all_items)*100 <= self.max_dataitems_per_worker and ((not score) or (score >= self.score_min))):
        	return True
        return False

    def score(self, user):
        score = False
        for answer in Answer.objects.filter(task__job = self.job, executor = user):
            if not score:
                score = answer.score
            else:
                score+=answer.score
        return score
