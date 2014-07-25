from django.db import models
from django.utils.timezone import now
from kitchen.models import Job

class Attachment(models.Model):
    job = models.ForeignKey(Job, null = True, blank = True)
    source_file = models.FileField(upload_to='attachments')

class Notification(models.Model):
    job = models.ForeignKey(Job, null = True, blank = True)
    last = models.DateField(auto_now=True,default=now())
