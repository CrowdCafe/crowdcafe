from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from forms import JobForm

import views

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    url(r'^$', views.Home, name='kitchen-home'),
    url(r'job/(?P<pk>\d+)/workers/$', views.JobWorkers, name='kitchen-job-workers'),
    
    url(r'job/create/$', login_required(views.JobCreation.as_view()), name='kitchen-job-create'),
    url(r'job/(?P<pk>\d+)/update/$', login_required(views.JobUpdate.as_view()), name='kitchen-job-update'),
    
    url(r'job/(?P<pk>\d+)/data/$', views.JobData, name='kitchen-job-data'),
    url(r'job/(?P<pk>\d+)/data/upload$', views.JobDataUpload, name='kitchen-job-data-upload'),

    url(r'job/(?P<pk>\d+)/quality/update/$', login_required(views.QualityControlUpdate.as_view()), name='kitchen-job-quality-update'),
)
