from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from .models import Email_details
from .forms import EmailForm
from django.http import HttpResponse, HttpResponseRedirect
import logging

logger = logging.getLogger(__name__)

# To handle index page
def index_view(request):
  return render(request, "application/index.html", {})

# To handle email information
def email_view(request):

    my_form = EmailForm(request.POST or None)
    if my_form.is_valid():

      csv_file = request.FILES.get("csv_file")
      csv_email_id = []
      if csv_file != None:
        if not csv_file.name.endswith('.csv'):
          messages.error(request,'File is not CSV type')
          return HttpResponseRedirect(reverse("myapp:upload_csv"))

        file_data = csv_file.read().decode("utf-8")
        csv_email_id = file_data.split("\n")

      subject = my_form.cleaned_data['subject']
      message = my_form.cleaned_data['body']
      from_email = settings.EMAIL_HOST_USER
      email_id_list = my_form.cleaned_data['email_id']
      cc_list = my_form.cleaned_data['cc']
      bcc_list = my_form.cleaned_data['bcc']
      to_list = email_id_list + csv_email_id

      email = EmailMessage(
          subject=subject,
          body=message,
          from_email=from_email,
          to=to_list,
          cc=cc_list,
          bcc=bcc_list,
          reply_to=[from_email]
        )

      try:
        # TODO: Put send_mail and save() in transaction
        email.send()
        my_form.save()
        # Clear form after email info in DB
        my_form = EmailForm()
        logger.info("email sent successfully")
      except BadHeaderError:
        logger.error("Error occured while sending email")
        return HttpResponse('Invalid header found.')
    context = {
      "form"  : my_form
    }

    return render(request, "application/email_details.html", context)
