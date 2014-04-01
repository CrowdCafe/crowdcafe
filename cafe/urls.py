from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    url(r'^$', views.Home, name='cafe-home'),
    url(r'welcome/$', views.Welcome, name='cafe-welcome'),
    url(r'tasks/$', views.TaskList, name='cafe-task-list'),
    url(r'tasks/(?P<task_id>\d+)/assign/$', views.TaskInstanceAssign, name='cafe-taskinstance-assign'),
    url(r'instance/(?P<instance_id>\d+)/$', views.TaskInstanceExecute, name='cafe-taskinstance-execute'),
)
