DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['localhost','crowdcafe.io']

# Settings for admin account, commission amount etc
# ---------------------------------------------------------------
BUSINESS = {
    'platform_owner_account_id': 1,
    'platform_commission': 0.3,
    'allow_debt':30
}
# ---------------------------------------------------------------
# Django settings for CrowdCafe project.
BROKER_URL = "amqp://guest:guest@localhost:5672//"