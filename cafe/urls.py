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
    url(r'profile/$', views.UserProfile, name='cafe-profile'),
    url(r'transactions/$', views.Transactions, name='cafe-transactions'),

    url(r'context/set/$', views.setContext, name='cafe-context-set'),
    
    url(r'jobs/$', views.JobList, name='cafe-job-list'),
    url(r'jobs/(?P<job_id>\d+)/assign/$', views.JobAssign, name='cafe-job-assign'),
    url(r'task/(?P<task_id>\d+)/$', views.TaskExecute, name='cafe-task-execute'),

    url(r'reward/(?P<reward_id>\d+)/purchase/$', views.RewardPurchase, name='cafe-reward-purchase'),
    url(r'coupon/(?P<coupon_id>\d+)/activate/$', views.CouponActivate, name='cafe-coupon-activate'),

    url(r'account/(?P<account_id>\d+)/remove/$', views.AccountRemove, name='cafe-account-remove'),

    url(r'task/(?P<task_id>\d+)/skip/$', views.TaskSkip, name='cafe-task-skip'),
    url(r'task/(?P<task_id>\d+)/complete/$', views.TaskComplete, name='cafe-task-complete'),
)
