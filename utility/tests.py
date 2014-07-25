"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.test.utils import override_settings

from account.models import Account, Membership
from kitchen.models import App, Job
from utility.utils import notifySuperUser, notifyMoneyAdmin



#NOTE: remove this if u wanto to send the email.
# @override_settings(EMAIL_BACKEND="djrill.mail.backends.djrill.DjrillBackend")
class MandrillTest(TestCase):
    def test_notifySU(self):
        self.group = Group.objects.create(name='superuser')
        self.user = User.objects.create(username='pavel', password='test', first_name="pavel",
                                        email="pavel@crowdcafe.io")
        self.group.user_set.add(self.user)
        self.user = User.objects.create(username='stefano', password='test', first_name="stefano",
                                        email="stefano@crowdcafe.io")
        self.group.user_set.add(self.user)
        # self.user

        self.account = Account.objects.create(title='test', creator=self.user)
        Membership.objects.create(user=self.user, account=self.account)
        self.app = App.objects.create(account=self.account, creator=self.user, title='test')

        self.job1 = Job.objects.create(app=self.app, creator=self.user, title='job title 1',
                                       description='job desc', category='CF', units_per_page='2', device_type='AD',
                                       judgements_webhook_url='http://example.com',
                                       userinterface_url="http://example.com/ui/")
        notifySuperUser(self.job1.id)


# @override_settings(EMAIL_BACKEND="djrill.mail.backends.djrill.DjrillBackend")
class MandrillTest(TestCase):
    def test_notifySU(self):
        self.user = User.objects.create(username='stefano', password='test', first_name="Stefano",
                                        email="stefano@crowdcafe.io")
        # self.user
        notifyMoneyAdmin(self.user, 2)
        notifyMoneyAdmin(self.user, 1)
        notifyMoneyAdmin(self.user, 0, 1.0)

