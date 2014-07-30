"""
This file is the test case for the Rewards.
"""
import json
from django.contrib.auth.models import User
from django.test import TestCase

from account.models import Account, Profile, FundTransfer
from account.utils import initUser
from rewards.models import Vendor, Reward, Coupon

class RewardTests(TestCase):
    '''
    testing the reward
    '''

    def setUp(self):
        '''
        setup the enviroment
        '''
        # Create reward provider
        User.objects.create(username='test_vendor', password='test', email="test1@test.com")
        self.reward_provider = User.objects.get(username='test_vendor')

        # Create worker
        User.objects.create(username='test_worker', password='test', email="test2@test.com")
        self.worker = User.objects.get(username='test_worker')

        # Give money to worker:
        FundTransfer.objects.create(to_account = self.worker.profile.personalAccount, from_account = self.reward_provider.profile.personalAccount, amount = 20, description = 'cash')
        
        # Create Vendor
        Vendor.objects.create(title='test_vendor', account = self.reward_provider.profile.personalAccount, creator = self.reward_provider)
        self.vendor = Vendor.objects.get(title='test_vendor')
        
        # Create Reward
        Reward.objects.create(title='reward_test', vendor = self.vendor, creator = self.reward_provider, cost_for_worker = 1, cost_for_platform = 0.5)
        self.reward = Reward.objects.get(title='reward_test')

        # Generate Coupons
        self.reward.generateCoupons(10)
        
    def test_purchasing_coupons(self):
        """
        Ensure that a a worker can buy something
        """

        coupon = self.reward.purchaseCoupon(self.worker)
        self.assertEqual(coupon.reward.title, 'reward_test')

        

