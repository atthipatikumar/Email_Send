from __future__ import absolute_import, unicode_literals
from celery import task
from .models import Email_details, Admin
from django.utils import timezone
import csv
from django.core.mail import EmailMessage
import itertools
import logging
logger = logging.getLogger(__name__)


@task()
def scheduled_email_report():
  time_range = timezone.now() - timezone.timedelta(minutes=30)
  objects = Email_details.objects.filter(created_at__gte=time_range)
  
  if not objects:
    logger.info("No emails found in last 30 minutes")
    return
  field_names = ['id', 'email_id', 'subject', 'body', 'cc', 'bcc',  'created_at']
  export_as_csv(objects, field_names)
  file = open('\kumar\Django-projects\details.csv')
  admin_emails = list(itertools.chain(*list(Admin.objects.values_list('email'))))
  logger.info("Sending mails to Admins:" + ", ".join(admin_emails))
  message = EmailMessage(
    'Email Report',
    'Please find attached CSV containing emails sent in last 30 mins',
    'help@mailservice.com',
    admin_emails,
    reply_to=[admin_emails[0]]
  )
  message.attach_file('\kumar\Django-projects\details.csv', mimetype='text/csv')
  message.send()
  logger.info("Email report sent successfully")



def export_as_csv(emails, fields):
  with open('\kumar\Django-projects\details.csv', 'w', newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
    fields = list(fields) 
    writer.writerow(fields)
    for email in emails:
      row = []
      for field in fields:
        row.append(getattr(email, field))
      writer.writerow(row)