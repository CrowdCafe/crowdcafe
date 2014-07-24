# TODO - needs to be rewritten
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

import views
urlpatterns = patterns('',
    # -------------------------------------------------------------------------------
    # ATTACHMENTS
    url(r'jobs/(?P<job_pk>\d+)/attachment/create/$', login_required(views.AttachmentCreateView.as_view()), name='attachment-create'),
    url(r'jobs/(?P<job_pk>\d+)/duplicate/$', login_required(views.duplicateJob), name='job-duplicate'),
    # COUPONS
    url(r'rewards/(?P<reward_pk>\d+)/coupons/generate/$', views.generateRewardCoupons, name='coupon-generate'),
    
  )
