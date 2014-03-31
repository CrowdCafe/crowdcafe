from django.conf.urls import patterns, include, url
#import views
import api
import views

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    url(r'auth/$', views.Auth, name='cafe-auth'),
    
    url(r'user/$', api.getUser, name='cafe-user'),
    url(r'tasks/$', api.getTasks, name='cafe-tasks-list'),
    url(r'tasks/(?P<task_id>\d+)/instance/$', api.getInstance, name='cafe-get-instance'),
)
