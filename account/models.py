from django.db import models
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from datetime import datetime 

class Profile(models.Model):
    user = models.OneToOneField(User) 
    def __unicode__(self):
        return str(self.id)
    @property
    def short_name(self):
        return self.user.first_name.encode('utf-8')+' '+self.user.last_name[:1].encode('utf-8')+'.'
    @property
    def full_name(self):
        return self.user.first_name.encode('utf-8')+' '+self.user.last_name.encode('utf-8')

    @property
    def logged_in_via_fb(self):
        if UserSocialAuth.objects.filter(user=self.user,provider='facebook').all().count()>0:
            return True
        else:
            return False 

    @property
    def url(self):
        if self.logged_in_via_fb:
            return 'https://facebook.com/'+str(self.user.username.encode('utf-8'))
        else:
            return 'http://www.gravatar.com/' + hashlib.md5(self.user.email.lower()).hexdigest() 
#------------------------