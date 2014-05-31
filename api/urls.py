from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='api-home'),
	url(r'token/$', views.home, name='api-home'),
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    url(r'user/$', views.getUser, name='api-user'),
    url(r'jobs/$', views.getJobs, name='api-tasks-list'),
    url(r'jobs/(?P<job_id>\d+)/task/$', views.getTask, name='api-get-instance'),

    url(r'jobs/(?P<job_id>\d+)/items/upload/$', views.uploadItems, name='api-job-upload-items'),
    
    url(r'jobs/(?P<job_id>\d+)/answers/$', views.getAnswers, name='api-job-answers'),
    url(r'jobs/(?P<job_id>\d+)/csv/$', views.getCSV, name='api-job-csv'),
    url(r'wikipedia/read/$', views.readUrl, name='api-url-read'),
)
