from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    
    url(r'user/$', views.getUser, name='api-user'),
    url(r'tasks/$', views.getTasks, name='api-tasks-list'),
    url(r'tasks/(?P<task_id>\d+)/instance/$', views.getInstance, name='api-get-instance'),

    url(r'tasks/(?P<task_id>\d+)/answers/$', views.getAnswers, name='api-task-answers'),
)
