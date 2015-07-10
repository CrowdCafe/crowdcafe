# SOCIAL AUTH CREDENTIALS
# ---------------------------------------------------------------
# Facebook
import os
FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_API_SECRET = os.environ.get('FACEBOOK_API_SECRET')
# Google
GOOGLE_OAUTH2_CLIENT_ID      = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET  = os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET')
GOOGLE_DISPLAY_NAME = os.environ.get('GOOGLE_DISPLAY_NAME')
# Github
GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID')
GITHUB_API_SECRET = os.environ.get('GITHUB_API_SECRET')
# ---------------------------------------------------------------
 
# PayPal account on which requestors send money
# ---------------------------------------------------------------
PAYPAL_RECEIVER_EMAIL = os.environ.get('PAYPAL_RECEIVER_EMAIL')
PAYPAL_TEST = False
# ---------------------------------------------------------------
 
 
# AMAZON AWS CREDENTIALS FOR STORING STATIC FILES AND ATTACHMENTS (see utilities)
# -----------------------------------------------------------------------------
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.environ.get('AWS_REGION')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
STATIC_URL = 'https://s3-eu-west-1.amazonaws.com/'+AWS_STORAGE_BUCKET_NAME+'/'
 
 
# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('SECRET_KEY')
# -----------------------------------------------------------------------------
 
# EMAILS
# -----------------------------------------------------------------------------
# TODO: fix the key when in production with one that can be used only by the ip of the server
MANDRILL_API_KEY = os.environ.get('MANDRILL_API_KEY')
EMAIL_HOST_PASSWORD = MANDRILL_API_KEY
EMAIL_HOST_USER = 'pavel@crowdcafe.io'
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
SERVER_EMAIL = 'error@crowdcafe.io'
 
# TODO: change accordingly to the webhook of mailchimp
MC_KEY = os.environ.get('MC_KEY')

OPBEAT = {
    "ORGANIZATION_ID": os.environ.get('OPBEAT_ORGANIZATION_ID'),
    "APP_ID": os.environ.get('OPBEAT_APP_ID'),
    "SECRET_TOKEN": os.environ.get('OPBEAT_SECRET_TOKEN'),
    "DEBUG" : True
}
# -----------------------------------------------------------------------------
#comment