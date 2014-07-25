import logging
import re
import csv
from datetime import datetime

from django.contrib.auth.models import Group
from django.core.mail.message import EmailMultiAlternatives
from django.core.urlresolvers import reverse
import scraperwiki
from django.core.mail import EmailMessage

from CrowdCafe.settings_local import DEBUG
from kitchen.models import Job, Unit
from utility.models import Notification


def saveUnits(job, dataset):
    units = []
    if len(dataset) > 0:
        for item in dataset:
            dataitem = Unit(job=job, input_data=item)
            dataitem.save()

            units.append(dataitem.id)
    return units


def collectDataFromCSV(url):
    dataset = []

    pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
    data = scraperwiki.scrape(url)
    reader = csv.reader(data.splitlines(), delimiter=';')

    i = 0
    for row in reader:
        if i == 0:
            headers = row
        else:
            dataitem = {}
            for j in range(len(row)):
                dataitem[headers[j]] = pattern.sub(u'\uFFFD', row[j]).decode('latin-1').encode("utf-8")
            dataset.append(dataitem)
        i += 1
    return dataset


log = logging.getLogger(__name__)


def sendEmail(sender, title, html, email):
    html += '<br/> <a href="http://crowdcafe.io">Crowd Computer</a>'

    msg = EmailMultiAlternatives(
        subject=title,
        body=html,
        from_email=sender,  # + ' (CrowdComputer)',
        to=[email]
    )
    log.debug('test')
    msg.attach_alternative(html, "text/html")
    msg.send()
    return True


def notifySuperUser(job_id):
    log.debug(job_id)
    job = Job.objects.get(pk=job_id)
    last_notification, created = Notification.objects.get_or_create(job=job)
    # SQLLIte use string so skip it when debug
    if DEBUG or last_notification.last < datetime.today().date() or created:
        group = Group.objects.get(name='superuser')
        superUsers = group.user_set.all()
        emails = superUsers.values_list('email', flat=True)
        log.debug(emails)
        msg = EmailMessage(subject="New Task Available",
                           from_email="CrowdCafe notification <notifications@crowdcafe.io>",
                           to=emails)
        # TODO: change with correct template
        msg.template_name = "NOTIFICATION_SU"
        # put here the variables for all the data that have to be changed for ALL the users
        msg.global_merge_vars = {
            'TASK_TITLE': job.title,
            'TASK_DESCRIPTION': job.description,
            'TASK_URL': "<a href='http://www.crowdcafe.io/" + reverse('cafe-units-assign',
                                                                      args=(job_id,)) + "'>DO IT NOW!</a>"
        }
        mail_names = superUsers.values_list('email', 'first_name')
        vars = {}
        for mail_name in mail_names:
            vars[mail_name[0]] = {"USER": mail_name[1]}
            # 'stefano.tranquillini@gmail.com': {'USER': "Ste"},

        # this sets the variable for each user, in this case the name
        msg.merge_vars = vars
        # use info from the template, check on the mandrill website.
        msg.async = True
        msg.use_template_subject = True
        msg.use_template_from = True
        msg.send()
    else:
        log.debug('notification too close')


_good = ('Your account has been charged', 'Your account has been topped up of %s.')
_bad = ('Problem with your account', 'We encountred a problem with your account. %s')
_no_credit = ('Your credit is insufficient', 'Your credit is insufficient to execute the operation you required. %s')


def notifyMoneyAdmin(account, status, info=''):
    message = _good
    if status==1:
        message = _bad
    if status ==2:
        message = _no_credit
    if account.email:
        emails = [account.email]
    elif account.creator.email:
        emails = [account.creator.email]
    else:
        return
    log.debug(emails)
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
