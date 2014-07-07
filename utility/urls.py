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
    # COUPONS
    url(r'rewards/(?P<reward_pk>\d+)/coupons/generate/$', views.generateRewardCoupons, name='coupon-generate'),
    
  )
