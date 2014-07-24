from os.path import join, normpath
from settings_common import *
from settings_sensitive import *

ALLOWED_HOSTS = ['localhost','crowdcafe.io']
DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

APP_URL ='http://5.101.96.187'

'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'crowdcafe', # Or path to database file if using sqlite3.
        'USER': 'root', # Not used with sqlite3.
        'PASSWORD': 'root', # Not used with sqlite3.
        'HOST': '/Applications/MAMP/tmp/mysql/mysql.sock', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
        "init_command": "SET foreign_key_checks = 0;",
        },
    }
}'''
# CrowdCafe_local
FACEBOOK_APP_ID = 'YOUR_FACEBOOK_APP_ID'
FACEBOOK_API_SECRET = 'YOUR_FACEBOOK_API_SECRET'

GOOGLE_OAUTH2_CLIENT_ID      = 'GOOGLE_OAUTH2_CLIENT_ID'
GOOGLE_OAUTH2_CLIENT_SECRET  = 'GOOGLE_OAUTH2_CLIENT_SECRET'

GOOGLE_DISPLAY_NAME = 'CrowdCafe'

TWITTER_CONSUMER_KEY='TWITTER_CONSUMER_KEY'
TWITTER_CONSUMER_SECRET='TWITTER_CONSUMER_SECRET'

GITHUB_APP_ID = 'GITHUB_APP_ID'
GITHUB_API_SECRET = 'GITHUB_API_SECRET'

INSTAGRAM_CLIENT_ID = 'INSTAGRAM_CLIENT_ID'
INSTAGRAM_SECRET = 'INSTAGRAM_SECRET'

DROPBOX_APP_ID = 'DROPBOX_APP_ID'
DROPBOX_API_SECRET = 'DROPBOX_API_SECRET'

BUSINESS = {
    'platform_owner_account_id': 1,
    'platform_commission': 0.3,
    'allow_debt':30
}

# THIS IS THE TEST ONE - CHANGE IT LATER ON TO PRODUCTION VALUES
PAYPAL_RECEIVER_EMAIL = "pavel-facilitator@kucherbaev.com"
PAYPAL_TEST = True
PAYPAL_API_URL = 'https://api-3t.sandbox.paypal.com/nvp'
PAYPAL_LOGIN_URL = (
    'https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token='
)