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
    #url(r'job/new/$', views.JobNew, name='kitchen-job-new'),
    #url(r'job/save/$', views.JobSave, name='kitchen-job-save'),
    #url(r'job/(?P<job_id>\d+)/status/(?P<status>\w+)/$', views.JobStatusChange, name='kitchen-job-status-change'),

    #url(r'job/(?P<job_id>\d+)/ui/refresh/$', views.JobUIrefresh, name='kitchen-job-ui-refresh'),
    url(r'job/(?P<pk>\d+)/workers/$', views.JobWorkers, name='kitchen-job-workers'),
    
    url(r'job/create/$', login_required(views.JobCreation.as_view()), name='kitchen-job-create'),
    url(r'job/(?P<pk>\d+)/update/$', login_required(views.JobUpdate.as_view()), name='kitchen-job-update'),
    
    url(r'job/(?P<pk>\d+)/data/$', views.JobData, name='kitchen-job-data'),
    url(r'job/(?P<pk>\d+)/data/upload$', views.JobDataUpload, name='kitchen-job-data-upload'),

    url(r'job/(?P<pk>\d+)/quality/update/$', login_required(views.QualityControlUpdate.as_view()), name='kitchen-job-quality-update'),
   # url(r'celery/$', views.test_celery, name='kitchen-test'),
   )
