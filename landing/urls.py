from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    #===============================================================================
    # Views
    #-------------------------------------------------------------------------------
    url(r'^$', views.Home, name='home'),
    url(r'^welcome/$', views.Welcome, name='welcome'),
    url(r'^error/$', views.Error, name='error'),
)
