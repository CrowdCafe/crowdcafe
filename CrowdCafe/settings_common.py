#!/usr/bin/env python
#coding: utf8 

import os
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."),
)
# Django settings for CrowdCafe project.
BROKER_URL = "amqp://guest:guest@localhost:5672//"

GITHUB_HTML_TEMPLATES = {
    'owner':'CrowdCafe',
    'repository':'crowdcafe-ui-templates'
}

TASK_CATEGORIES = {
    'CF':{
        'id':'CF',
        'title':'Espresso',
        'cost':0.03,
        'icon':'landing/img/logo100_black.png',
        'time':'10 sec',
        'description':'Mostly clicking and swiping.',
        'examples': 'pair comparison, tag an object on an image, tweets sentiment, other simple tasks...'
    },
    'CP':{
        'id':'CP',
        'title':'Cappuccino',
        'cost':0.33,
        'icon':'libs/icons8/coffee-50.png',
        'time':'2 min',
        'description':'Some typing, some learning.',
        'examples':'make a photo of an object, short survey, receipt transcription, other medium-size tasks...'
        
    },
    'WN':{   
        'id':'WN',
        'title':'Wine',
        'cost':1,
        'icon':'libs/icons8/wine_bottle-50.png',
        'time':'6 min',
        'description':'Custom tasks.',
        'examples':'interview record, video capturing, complex information search, other non trivial tasks...'
    },
    'ZT':{
        'id':'ZT',
        'title':'Volunteering',
        'cost':0,
        'icon':'libs/icons8/like-50.png',
        'time':'any',
        'description':'simple',
        'examples': 'tasks without any reward'
    },
}
TASK_CATEGORIES_DICTIONARY = (('CF','Espresso'),('CP','Cappuccino'),('WN','Wine'),('ZT','Volunteering'),)



ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_ROOT, 'components')

BOWER_INSTALLED_APPS = (
    'bootstrap',
    'minimal-devices',
    'fontawesome',
    'BrandButtons',
    'framework7',
    'startup-demo',
    'raphael',
    'jquery'
)

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
    'cafe.context_processors.task_categories',
    'cafe.context_processors.cafe_context'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'social_auth.middleware.SocialAuthExceptionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'CrowdCafe.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'CrowdCafe.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

CRISPY_TEMPLATE_PACK = 'bootstrap3' 

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_auth',
    'mobi',
    'crispy_forms',
    'storages',
    'landing',
    'account',
    'kitchen',
    'preselection',
    'qualitycontrol',
    'api',
    'cafe',
    'rewards',
    'events',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'requests',
    'djangobower'
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
#    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
#    'social_auth.backends.google.GoogleBackend',
#    'social_auth.backends.yahoo.YahooBackend',
#    'social_auth.backends.browserid.BrowserIDBackend',
#    'social_auth.backends.contrib.linkedin.LinkedinBackend',
#    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
#    'social_auth.backends.contrib.orkut.OrkutBackend',
#    'social_auth.backends.contrib.foursquare.FoursquareBackend',
    'social_auth.backends.contrib.github.GithubBackend',
#    'social_auth.backends.contrib.vkontakte.VKontakteBackend',
#    'social_auth.backends.contrib.live.LiveBackend',
#    'social_auth.backends.contrib.skyrock.SkyrockBackend',
#    'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
#    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_ENABLED_BACKENDS = ('twitter','facebook','github','google-oauth2')

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.user.update_user_details',
    'social_auth.backends.pipeline.social.load_extra_data',
    'account.pipes.get_user_addinfo',
)

REST_FRAMEWORK = {
# Use hyperlinked styles by default.
# Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer'
    ,
    #'DEFAULT_RENDERER_CLASSES': (
    #    'rest_framework_csv.renderers.CSVRenderer',
    #),
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    #'DEFAULT_PERMISSION_CLASSES': [
    #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    #]
}

FACEBOOK_EXTENDED_PERMISSIONS = ['email']
GITHUB_EXTENDED_PERMISSIONS = ['user:email']
GOOGLE_EXTENDED_PERMISSIONS = ['email']

SOCIAL_AUTH_BACKEND_ERROR_URL = '/welcome/'
LOGIN_ERROR_URL = '/welcome/'
LOGIN_URL='/welcome/'
LOGIN_REDIRECT_URL = '/'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
        'GET'
    )
CORS_ALLOW_HEADERS = (
        'x-requested-with',
        'content-type',
        'accept',
        'origin',
        'authorization',
        'x-csrftoken'
    )



# -----------------------------------------------------------------------------
#DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'



STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'