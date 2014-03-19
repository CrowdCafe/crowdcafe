from os.path import join, normpath
from settings_common import *
from settings_sensitive import *

DATABASES = {
    'default': {
		'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ENTER_YOUR_DATABASE_NAME', # Or path to database file if using sqlite3.
        'USER': 'ENTER_YOUR_USERNAME', # Not used with sqlite3.
        'PASSWORD': 'ENTER_YOUR_PASSWORD', # Not used with sqlite3.
        'HOST': '/Applications/MAMP/tmp/mysql/mysql.sock', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
        "init_command": "SET foreign_key_checks = 0;",
        },
    }
}

# ENTER YOUR OWN CREDENTIALS:
# CrowdCafe_local
FACEBOOK_APP_ID = ''
FACEBOOK_API_SECRET = ''

GOOGLE_CONSUMER_KEY =''
GOOGLE_CONSUMER_SECRET = ''

GOOGLE_OAUTH2_CLIENT_ID      = ''
GOOGLE_OAUTH2_CLIENT_SECRET  = ''

GOOGLE_DISPLAY_NAME = 'CrowdCafe'