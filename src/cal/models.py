from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
	calendar_owner = models.ForeignKey(User)
	name = models.CharField(max_length=60, null=False, blank=False)
	color = models.CharField(max_length=12, null=False, blank=False)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.name


class Appointment(models.Model):
	calendar = models.ForeignKey(Calendar)
	title = models.CharField(max_length=60, blank=False, null=False)
	description = models.TextField(null=True, blank=True)
	start_date = models.DateTimeField(null=False, blank=False)
	end_date = models.DateTimeField(null=False, blank=False)

	def __str__(self):
		return self.title


class ShareRights(models.Model):
	code = models.IntegerField(null=False, blank=False)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.code

class AppointmentShare(models.Model):
	appointment = models.ForeignKey(Appointment)
	share_rights = models.ForeignKey(ShareRights)
	share_with = models.ForeignKey(User)

class CalendarShare(models.Model):
	calendar = models.ForeignKey(Calendar)
	share_rights = models.ForeignKey(ShareRights)
	share_with = models.ForeignKey(User)
