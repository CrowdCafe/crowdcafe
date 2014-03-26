from django.conf.urls import patterns, include, url
#import views
import api

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    url(r'tasks/$', api.getTasks, name='cafe-tasks-list'),
    url(r'tasks/(?P<task_id>\d+)/instance/$', api.getInstance, name='cafe-get-instance'),
)
