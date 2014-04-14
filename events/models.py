from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

#=========================================================================
# EVENTS
#=========================================================================

class Event(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    
    page = models.CharField(max_length = 32,  null=True, blank=True)    
    url = models.URLField(max_length = 256,  null=True, blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    context = models.CharField(max_length = 64,  null=True, blank=True)    
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.id
    