"""
This file is the test case for the API.
"""
import json
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from account.models import Account, Membership
from kitchen.models import App, Job


class AccountTests(APITestCase):
    '''
    testing the account
    '''

    def setUp(self):
        '''
         setup the enviroment
        '''
        User.objects.create(username='test', password='test', email="test@test.com")
        self.user = User.objects.get(username='test')
        token = Token.objects.get(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


    def test_me(self):
        """
        Ensure that a user can retrive his data
        """
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class AppTests(APITestCase):
    def setUp(self):
        '''
         setup the enviroment
        '''
        User.objects.create(username='test', password='test', email="test@test.com")
        self.user = User.objects.get(username='test')
        token = Token.objects.get(user=self.user)
        self.client = APIClient()
        self.app = App.objects.create(account=self.user.profile.personalAccount, creator=self.user, title='test')

        token = 'Token ' + token.key + '|' + self.app.token
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_list(self):
        App.objects.create(account=self.user.profile.personalAccount, creator=self.user, title='test 2')
        url = reverse('api-app-list')
        response = self.client.get(url)
        # check if the list has 1 element
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


        # check if the data are the same

    def test_detail(self):
        # mine: 200
        url = reverse('api-app-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"title": "test", "account": "personal account", "creator": "test"})

        # someone else trying to access mine
        client = APIClient()
        # another user SAME APP: OK
        user = User.objects.create(username='test2', password='test2', email="test@test.com")
        Membership.objects.create(user=user, account=self.user.profile.personalAccount)
        token = Token.objects.get(user=user)
        token = 'Token ' + token.key + '|' + self.app.token
        client.credentials(HTTP_AUTHORIZATION=token)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #someoneelse : 404
        url = reverse('api-app-detail', kwargs={'pk': 2})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class JobTests(APITestCase):
    def setUp(self):
        '''
         setup the enviroment
        '''
        self.user =User.objects.create(username='test', password='test', email="test@test.com")
        # self.user
        token = Token.objects.get(user=self.user)
        self.client = APIClient()

        self.account = Account.objects.create(title='test', creator=self.user)
        Membership.objects.create(user=self.user, account=self.account)
        self.app = App.objects.create(account=self.account, creator=self.user, title='test')

        token = 'Token ' + token.key + '|' + self.app.token
        self.client.credentials(HTTP_AUTHORIZATION=token)

        self.user2 = User.objects.create(username='usernew', password='test3', email="test@test.com")
        self.account2 = Account.objects.create(title='accountnew', creator=self.user2)
        Membership.objects.create(user=self.user2, account=self.account2)
        self.app2= App.objects.create(account=self.account2, creator=self.user2, title='appnew')

        self.job1=Job.objects.create(app=self.app, creator=self.user, title='job title 1',
                           description='job desc', category='CF', units_per_page='2', device_type='AD',
                           judgements_webhook_url='http://example.com', userinterface_url="http://example.com/ui/")
        self.job2=Job.objects.create(app=self.app2, creator=self.user2, title='job title 2',
                           description='job desc', category='CF', units_per_page='2', device_type='AD',
                           judgements_webhook_url='http://example.com', userinterface_url="http://example.com/ui/")

    def test_list(self):

        url = reverse('api-job-list')
        response = self.client.get(url)
        # check if the list has 1 element
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'],1)

    def test_detail(self):

        url = reverse('api-job-detail', kwargs={'pk': self.job1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'job title 1')

        # unexisting or of someone else: 404
        url = reverse('api-job-detail', kwargs={'pk':  0})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # setting back the correct url
        url = reverse('api-job-detail', kwargs={'pk':  self.job1})
        client = APIClient()
        # another user SAME APP: OK
        user = User.objects.create(username='test2', password='test2', email="test@test.com")
        Membership.objects.create(user=user, account=self.account)
        token = Token.objects.get(user=user)
        token = 'Token ' + token.key + '|' + self.app.token
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # another user, another app: 404

        token = Token.objects.get(user=self.user2)

        token = 'Token ' + token.key + '|' + self.app2.token
        client.credentials(HTTP_AUTHORIZATION=token)
        response = client.get(url, format='json')
        # this is not 403 beacuse the list is restricted by the app (see get_queryset)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create(self):
        # create not allowed : 405
        url = reverse('api-job-list')
        data = {'app': self.app.pk, 'creator': self.user.pk, 'title': 'api creation', 'description': 'api'}
        response = self.client.post(url, data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)



class UnitTest(APITestCase):
    def setUp(self):
        '''
         setup the enviroment
        '''
        self.user =User.objects.create(username='test', password='test', email="test@test.com")
        # self.user
        token = Token.objects.get(user=self.user)
        self.client = APIClient()

        self.account = Account.objects.create(title='test', creator=self.user)
        Membership.objects.create(user=self.user, account=self.account)
        self.app = App.objects.create(account=self.account, creator=self.user, title='test')

        token = 'Token ' + token.key + '|' + self.app.token
        self.client.credentials(HTTP_AUTHORIZATION=token)
        self.job =Job.objects.create(app=self.app, creator=self.user, title='job title 2',
                           description='job desc', category='CF', units_per_page='2', device_type='AD',
                           judgements_webhook_url='http://example.com', userinterface_url="http://example.com/ui/")

    def test_unit_list(self):


        url = reverse('api-unit-list', kwargs={'job_pk': self.job.pk})
        # print url
        # first element is an array
        data =  [[{'title':1},{'test':'as'}],{'title':2},{'title':3}]
        response = self.client.post(url, data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check the list

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # they are paginated
        # check the data of the first
        self.assertEqual(response.data['count'],3)
        self.assertEqual(response.data['results'][0]['input_data'],[{'title':1},{'test':'as'}])

        # add to an unexisting Job: 404
        url = reverse('api-unit-list', kwargs={'job_pk': 2000})
        data =  [[{'title':1},{'test':'as'}],{'title':2},{'title':3}]
        response = self.client.post(url, data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        #
        #
        client = APIClient()
        #  Another user, same APP: 201
        user =User.objects.create(username='test2', password='test2', email="test@test.com")
        Membership.objects.create(user=user, account=self.account)
        token = Token.objects.get(user=user)
        token = 'Token ' + token.key + '|' + self.app.token
        client.credentials(HTTP_AUTHORIZATION=token)
        url = reverse('api-unit-list', kwargs={'job_pk': self.job.pk})
        data =  [[{'title':1},{'test':'as'}],{'title':2},{'title':3}]
        response = client.post(url, data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Another user, different APP: 404
        user = User.objects.create(username='test4', password='test4', email="test@test.com")
        account = Account.objects.create(title='test4', creator=user)
        Membership.objects.create(user=user, account=account)
        token = Token.objects.get(user=user)
        app = App.objects.create(account=account, creator=user, title='test4')
        token = 'Token ' + token.key + '|' + app.token
        client.credentials(HTTP_AUTHORIZATION=token)
        url = reverse('api-unit-list', kwargs={'job_pk': 1})
        response = client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data =  [[{'title':1},{'test':'as'}],{'title':2},{'title':3}]
        response = client.post(url, data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unit_detail_get(self):
        url = reverse('api-unit-list', kwargs={'job_pk': self.job.pk})
        # first element is an array
        data =  [[{'title':1},{'test':'as'}],{'title':2},{'title':3}]
        response = self.client.post(url, data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url, format='json')
        first_unit = response.data['results'][0]['pk']


        url = reverse('api-unit-detail', kwargs={'job_pk': self.job.pk,'pk':first_unit})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['input_data'],[{'title':1},{'test':'as'}])

        client = APIClient()
        #  Another user, same APP: 201
        user =User.objects.create(username='test2', password='test2', email="test@test.com")
        Membership.objects.create(user=user, account=self.account)
        token = Token.objects.get(user=user)
        token = 'Token ' + token.key + '|' + self.app.token
        client.credentials(HTTP_AUTHORIZATION=token)
        response = client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['input_data'],[{'title':1},{'test':'as'}])

        # Another user, different APP: 404
        user = User.objects.create(username='test4', password='test4', email="test@test.com")
        account = Account.objects.create(title='test4', creator=user)
        Membership.objects.create(user=user, account=account)
        token = Token.objects.get(user=user)
        app = App.objects.create(account=account, creator=user, title='test4')
        token = 'Token ' + token.key + '|' + app.token
        client.credentials(HTTP_AUTHORIZATION=token)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
