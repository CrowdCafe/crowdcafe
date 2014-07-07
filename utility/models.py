from django.db import models
from kitchen.models import Job

class Attachment(models.Model):
    job = models.ForeignKey(Job, null = True, blank = True)
    source_file = models.FileField(upload_to='attachments', blank = True)