from django.db import models
from django.utils import timezone


class Admin(models.Model):
  username    = models.CharField(max_length=100)
  password    = models.CharField(max_length=50)
  email       = models.EmailField()

  def __str__(self):
        return self.username


class Email_details(models.Model):
  email_id      = models.CharField(max_length=120)
  subject       = models.CharField(max_length=120)
  body          = models.TextField()
  cc            = models.CharField(max_length=120, null=True)
  bcc           = models.CharField(max_length=120, null=True)
  created_at    = models.DateTimeField()
  updated_at    = models.DateTimeField()

  def save(self, *args, **kwargs):
    if not self.id:
      self.created_at = timezone.now()
      self.updated_at = timezone.now()
    return super(Email_details, self).save(*args, **kwargs)


