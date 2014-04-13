from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    url(r'^$', views.Home, name='cafe-home'),
    url(r'welcome/$', views.Welcome, name='cafe-welcome'),
    
    url(r'about/$', views.About, name='cafe-about'),
    url(r'rewards/$', views.Rewards, name='cafe-rewards'),
    url(r'transactions/$', views.Transactions, name='cafe-transactions'),
    
    url(r'tasks/$', views.TaskList, name='cafe-task-list'),
    url(r'tasks/(?P<task_id>\d+)/assign/$', views.TaskInstanceAssign, name='cafe-taskinstance-assign'),
    url(r'instance/(?P<instance_id>\d+)/$', views.TaskInstanceExecute, name='cafe-taskinstance-execute'),

    url(r'reward/(?P<reward_id>\d+)/purchase/$', views.RewardPurchase, name='cafe-reward-purchase'),
    url(r'coupon/(?P<coupon_id>\d+)/activate/$', views.CouponActivate, name='cafe-coupon-activate'),

    url(r'instance/(?P<instance_id>\d+)/skip/$', views.TaskInstanceSkip, name='cafe-taskinstance-skip'),
    url(r'instance/(?P<instance_id>\d+)/complete/$', views.TaskInstanceComplete, name='cafe-taskinstance-complete'),
)
