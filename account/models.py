from django.db import models
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from datetime import datetime 
from django.db.models import Q

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
    def connectedSocialNetworks(self):
        return UserSocialAuth.objects.filter(user=self.user).all()
    @property
    def avatar(self):
        if len(self.connectedSocialNetworks)>0:
            return "http://avatars.io/"+self.connectedSocialNetworks.reverse()[0].provider+"/"+str(self.connectedSocialNetworks.reverse()[0].uid)+"?size=medium"    
        else:
            return 'http://www.gravatar.com/' + hashlib.md5(self.user.email.lower()).hexdigest() 
        #if self.logged_in_via_fb:
        #    return 'https://facebook.com/'+str(self.user.username.encode('utf-8'))
        #else:
        #    return 'http://www.gravatar.com/' + hashlib.md5(self.user.email.lower()).hexdigest() 

class Account(models.Model):
    profile = models.OneToOneField(Profile)

    total_deposit = models.FloatField(default = 0)
    total_earning =  models.FloatField(default = 0)
    total_spending =  models.FloatField(default = 0)

    @property
    def balance(self):
        #return "{0:.2f}".format(self.total_deposit + self.total_earning - self.total_spending)
        return self.total_deposit + self.total_earning - self.total_spending
    @property
    def transactions(self):
        return AccountTransaction.objects.filter(Q(from_account=self) | Q(to_account=self)).order_by('-date_created').all()

CURRENCY_TYPE = (('RM','real'),('VM','virtual'))

class AccountTransaction(models.Model):

    from_account = models.ForeignKey(Account, related_name = 'from_account', blank = True, null = True)
    to_account = models.ForeignKey(Account, related_name = 'to_account', blank = True, null = True)

    currency = models.CharField(max_length=2, choices=CURRENCY_TYPE)
    amount = models.FloatField(default = 0)

    date_created = models.DateTimeField(auto_now_add=True, auto_now=False) 
    description = models.CharField(max_length=1000, blank = True)

    def save(self, *args, **kwargs):
        if self.pk is None:    

            if (self.from_account != self.to_account):
                self.from_account.total_spending += self.amount
                self.to_account.total_earning += self.amount

                self.to_account.save()
                self.from_account.save()
            else:
                self.to_account.total_spending += self.amount
                self.to_account.total_earning += self.amount
                # save only once - otherwise we face a bug
                self.to_account.save()

        super(AccountTransaction, self).save(*args, **kwargs)