from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    #url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('landing.urls')),
    url(r'', include('social_auth.urls')),
    url(r'kitchen/', include('kitchen.urls')),
    url(r'cafe/', include('cafe.urls')),
    url(r'api/', include('api.urls')),
    url(r'user/', include('account.urls')),
    url(r'rewards/', include('rewards.urls')),
    )
