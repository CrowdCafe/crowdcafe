# TODO - needs to be rewritten
from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import me, job_router, unit_router
import views


urlpatterns = patterns('',
                       url(r'^', include(views.router.urls)),
                       url(r'^', include(job_router.urls)),
                       url(r'^', include(unit_router.urls)),
                       url(r'^me/', me, name='me'),
                       url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token', name='token'),
)
urlpatterns = format_suffix_patterns(urlpatterns)
