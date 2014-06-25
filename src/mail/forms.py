from mail.models import MailAccount, MailHost
from django.forms import ModelForm, PasswordInput, CharField



class MailAccountForm(ModelForm):
	class Meta:
		model = MailAccount
		password = CharField(widget=PasswordInput)
		exclude = ['mail_account_owner', 'send_host', 'retrieve_host']
		widgets = { 'password': PasswordInput()}


class MailHostForm(ModelForm):
	class Meta:
		model = MailHost
		exclude = ['send_host_of', 'retrieve_host_of']		