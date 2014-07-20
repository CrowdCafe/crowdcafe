from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from rest_framework.authtoken.models import Token
from social_auth.models import UserSocialAuth
from decimal import Decimal
from django.db.models import Sum
import hashlib
from django.db.models.signals import post_save
from paypal.standard.ipn.signals import payment_was_successful



# Extension of User class to add some properties (does not have any columns)
class Profile(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return str(self.id)

    @property
    def shortname(self):
        return self.user.first_name.encode('utf-8') + ' ' + self.user.last_name[:1].encode('utf-8') + '.'

    @property
    def fullname(self):
        return self.user.first_name.encode('utf-8') + ' ' + self.user.last_name.encode('utf-8')

    # get a list of networks which are connected to the user
    # if networks is defined then function will return only out of this list
    def connectedSocialNetworks(self, networks):
        connected = UserSocialAuth.objects.filter(user=self.user)
        if networks:
            connected = connected.filter(provider__in = networks)
        return connected.all()
    # gets a personal account from the list of all accounts of this user
    @property
    def personalAccount(self):
        return Account.objects.filter(personal = self.user, creator = self.user).all()[0]
    
    @property
    def avatar(self):
        # we use http://avatars.io/ to show avatars
        base_url = "http://avatars.io/"
        avatars_io_networks = ['twitter','facebook','instagram']
        
        if len(self.connectedSocialNetworks(avatars_io_networks)) > 0:
            return base_url + self.connectedSocialNetworks(avatars_io_networks).reverse()[0].provider + "/" + str(
                self.connectedSocialNetworks(avatars_io_networks).reverse()[0].uid) + "?size=medium"
        else:
            # try to get an avatar from gravatar
            return base_url +'gravatar/'+ hashlib.md5(self.user.email.lower()).hexdigest()

            
# Class for grouping several users to one billing account. Can be useful - if there is an organization, or a research team, which consists of 3 people working together.

class Account(models.Model):
    users = models.ManyToManyField(User, through='Membership')
    title = models.CharField(max_length=256)
    personal = models.BooleanField(default=False)
    creator = models.ForeignKey(User, related_name='Creator')
    #sum of all fundtransfer amounts, where to_account = self (we keep it as a column to do less calls to aggregation of FundTransfer table)
    total_earnings = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total_spendings = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    #sum of all fundtransfer amounts, where from_account = self (we keep it as a column to do less calls to aggregation of FundTransfer table)
    deleted = models.DateTimeField(blank=True, null=True)
    # 'earnings', 'spendings'
    #TODO - make sure that when somebody creates account he can not modify total-earnings, total_spending.
    def recalculate(self):
        self.recalculateType('earnings');
        self.recalculateType('spendings');

    def recalculateType(self, total_type):
        if (total_type == 'earnings'):
            total_earnings = FundTransfer.objects.filter(to_account=self).aggregate(Sum('amount'))['amount__sum']
            if total_earnings:
                self.total_earnings = total_earnings
        elif (total_type == 'spendings'):
            total_spendings = FundTransfer.objects.filter(from_account=self).aggregate(Sum('amount'))['amount__sum']
            if total_spendings:
                self.total_spendings = total_spendings
        self.save()
    def __unicode__(self):
        return str(self.creator.profile.fullname+' '+self.title)
    # show current balance of an account (saldo)
    @property
    def balance(self):
        return self.total_earnings - self.total_spendings


MEMBERSHIP_TYPE = (('AN', 'Admin'), ('MR', 'Member'))


class Membership(models.Model):
    class Meta:
        unique_together = ['user', 'account']
    user = models.ForeignKey(User)
    account = models.ForeignKey(Account)
    permission = models.CharField(max_length=2, choices=MEMBERSHIP_TYPE, default='AN')
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)

# when a worker earns money - they go from requestor to a worker
# when a worker/requestor wants to send money to another user - they do it via fundtransfer

class FundTransfer(models.Model):
    from_account = models.ForeignKey(Account, related_name='from_account', blank=True, null=True)
    to_account = models.ForeignKey(Account, related_name='to_account', blank=True, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    description = models.CharField(max_length=1000, blank=True)  # when we generate transfers we might add here a description - what this transfer is for.

@receiver(post_save, sender=FundTransfer)
def recalculateAccount(sender, **kwargs):
    obj = kwargs['instance']

    if obj.from_account:
        obj.from_account.recalculate()
    if obj.to_account:
        obj.to_account.recalculate()
    return True

@receiver(post_save, sender=get_user_model())
def initUser(sender, **kwargs):
    user = kwargs['instance']
    # create a token for authorization via API
    token, created = Token.objects.get_or_create(user=user)
    
    # create a profile for using its properties 
    profile, created = Profile.objects.get_or_create(user=user)
    
    # create a personal account
    account, created = Account.objects.get_or_create(creator = user, personal = True, title = 'personal account')

    # add current user to this account with Admin permission
    membership, created = Membership.objects.get_or_create(user = user, permission = 'AN', account = account)

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == "Completed":
        # Undertake some action depending upon `ipn_obj`.
        account = get_object_or_404(Account, pk = ipn_obj.custom)
        deposit = FundTransfer(to_account = account, amount = ipn_obj.mc_gross, description = "PayPal invoice: "+ipn_obj.invoice+' transaction: '+ipn_obj.txn_id)
        deposit.save()

payment_was_successful.connect(show_me_the_money)