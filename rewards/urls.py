from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    url(r'^$', views.Home, name='rewards-home'),
    url(r'vendor/new/$', views.VendorNew, name='rewards-vendor-new'),
    url(r'vendor/save/$', views.VendorSave, name='rewards-vendor-save'),
    url(r'vendor/(?P<vendor_id>\d+)/reward/new/$', views.RewardNew, name='rewards-vendor-reward-new'),
    url(r'vendor/(?P<vendor_id>\d+)/reward/save/$', views.RewardSave, name='rewards-vendor-reward-save'),
    url(r'reward/(?P<reward_id>\d+)/instances/$', views.RewardInstances, name='rewards-vendor-reward-instances'),
    url(r'reward/(?P<reward_id>\d+)/instances/generate/$', views.RewardInstancesGenerate, name='rewards-vendor-reward-instances-generate'),
)
