from django.core.mail import EmailMessage

__author__ = 'stefano'


_good = ('Your account has been charged', 'Your account has been topped up of %s.')
_bad = ('Problem with your account', 'We encountred a problem with your account. %s')
_no_credit = ('Your credit is insufficient', 'Your credit is insufficient to execute the operation you required. %s')
_units_completed = ('Job is completed', 'We have noticed, that all the units of the job you were running are completed. %s')

def notifyMoneyAdmin(account, status, info=''):
    message = _good
    if status==1:
        message = _bad
    if status ==2:
        message = _no_credit
    if status ==3:
        message = _units_completed
    if account.email:
        emails = [account.email]
    elif account.creator.email:
        emails = [account.creator.email]
    else:
        return
    msg = EmailMessage(subject=message[0], from_email="CrowdCafe <team@crowdcafe.io>",
                       to=emails)
    msg.template_name = "MONEY_ADMIN"
    txt = str(message[1] % info)
    msg.global_merge_vars = {
        'MESSAGE': txt,
         "USER": account.title
    }
    msg.async = True
    msg.send()