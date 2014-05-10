from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	max_inbox_size = models.IntegerField(null=True, blank=True)
	max_no_mail_accounts = models.IntegerField(null=True, blank=True)
	max_no_calendars = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return str(self.username + " (" + self.first_name + " " + self.last_name + ")")