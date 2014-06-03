from mail.models import MailAccount, MailHost
from django.forms import ModelForm


class MailAccountForm(ModelForm):
	class Meta:
		model = MailAccount
		exclude = ['mail_account_owner', 'send_host', 'retrieve_host']


class MailHostForm(ModelForm):
	class Meta:
		model = MailHost
		exclude = ['send_host_of', 'retrieve_host_of']		