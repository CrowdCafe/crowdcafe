from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    url(r'^$', views.Home, name='kitchen-home'),
    url(r'task/new/$', views.TaskNew, name='kitchen-task-new'),
    url(r'task/save/$', views.TaskSave, name='kitchen-task-save'),
    url(r'task/(?P<task_id>\d+)/status/(?P<status>\w+)/$', views.TaskStatusChange, name='kitchen-task-status-change'),
    url(r'celery/$', views.test_celery, name='kitchen-test'),
)
