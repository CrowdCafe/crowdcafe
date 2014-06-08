from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    url(r'^$', views.Home, name='kitchen-home'),
    url(r'job/new/$', views.JobNew, name='kitchen-job-new'),
    url(r'job/save/$', views.JobSave, name='kitchen-job-save'),
    url(r'job/(?P<job_id>\d+)/status/(?P<status>\w+)/$', views.JobStatusChange, name='kitchen-job-status-change'),
    url(r'job/(?P<job_id>\d+)/data/$', views.JobData, name='kitchen-job-data'),
    url(r'job/(?P<job_id>\d+)/ui/refresh/$', views.JobUIrefresh, name='kitchen-job-ui-refresh'),
    url(r'job/(?P<job_id>\d+)/workers/$', views.JobWorkers, name='kitchen-job-workers'),
   # url(r'celery/$', views.test_celery, name='kitchen-test'),
   )
