from django.db import models
from django.contrib.auth.models import User



class MailHost(models.Model):
	host_name = models.CharField(max_length=60, null=False, blank=False)
	host_port = models.PositiveIntegerField(null=False, blank=False)
	host_ssl = models.BooleanField()
	host_authentication = models.BooleanField()

	def __str__(self):
		return str(self.host_name + ":" + str(self.host_port))

class MailAccount(models.Model):
	sender_name = models.CharField(max_length=60, null=True, blank=True)
	email = models.EmailField(max_length=60, null=False, blank=False)
	logon_name = models.CharField(max_length=60, null=False, blank=False)
	password = models.CharField(max_length=60, null=False, blank=False)
	mail_account_owner = models.ForeignKey(User)
	retrieve_host = models.OneToOneField(MailHost, related_name='retrieve_host_of')
	send_host = models.OneToOneField(MailHost, related_name='send_host_of')

	def __str__(self):
		if self.sender_name is not None:
			return str(self.email + " (" + self.sender_name + ")")
		else:
			return str(self.email)	


# class Message(models.Model):
# 	message_owner = models.ForeignKey(User)
# 	message_subject = models.CharField(max_length=180, blank=False, null=False)
# 	message_body = models.TextField(blank=True, null=True)
# 	message_sender = models.CharField(max_length=180, blank=False, null=False)
	


	
