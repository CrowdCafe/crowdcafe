from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    url(r'^$', views.Home, name='kitchen-home'),
    url(r'task/new/$', views.TaskNew, name='kitchen-task-new'),
    url(r'task/save/$', views.TaskSave, name='kitchen-task-save'),
)
