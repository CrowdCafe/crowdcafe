UPLOADCARE = {
    'pub_key': 'ENTER_YOUR_KEY',
    'secret': 'ENTER_YOUR_SECRET',
}

# AMAZON AWS CREDENTIALS------------------------------------------------------
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = 'ENTER_YOUR_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'ENTER_YOUR_ACCESS_SECRET'
AWS_REGION = 'https://s3-eu-west-1.amazonaws.com/'
AWS_STORAGE_BUCKET_NAME = 'ENTER_YOUR_BUCKET_NAME'
# -----------------------------------------------------------------------------

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'YOUR_SECRET'

# TODO: fix the key when in production with one that can be used only by the ip of the server
MANDRILL_API_KEY = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_HOST = ''
EMAIL_PORT = 0 #set correct one
SERVER_EMAIL = ''

# TODO: change accordingly to the webhook of mailchimp
MC_KEY = ''