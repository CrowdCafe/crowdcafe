from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

import views

urlpatterns = patterns('',
    #===============================================================================
    # General views
    #-------------------------------------------------------------------------------
    url(r'^$', views.Home, name='cafe-home'),
    url(r'welcome/$', views.Welcome, name='cafe-welcome'),
    
    url(r'about/$', views.About, name='cafe-about'),
    url(r'rewards/$', views.Rewards, name='cafe-rewards'),
    url(r'profile/$', views.UserProfile, name='cafe-profile'),
    url(r'transactions/$', views.Transactions, name='cafe-transactions'),
    url(r'jobs/$', login_required(views.JobListView.as_view()), name='cafe-job-list'),
    
    # Units execution
    url(r'jobs/(?P<job_id>\d+)/assign/$', views.UnitsAssign, name='cafe-units-assign'),
    url(r'jobs/(?P<job_id>\d+)/complete/$', views.UnitsComplete, name='cafe-units-complete'),

    # Rewards purchasing
    url(r'reward/(?P<reward_id>\d+)/purchase/$', views.RewardPurchase, name='cafe-reward-purchase'),
    url(r'coupon/(?P<coupon_id>\d+)/activate/$', views.CouponActivate, name='cafe-coupon-activate'),

    # Others
    url(r'context/set/$', views.setContext, name='cafe-context-set'),   
)
