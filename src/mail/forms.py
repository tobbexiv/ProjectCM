from mail.models import MailAccount, MailHost
from django.forms import ModelForm, PasswordInput, CharField, Form, EmailField, Textarea, ModelChoiceField
from django.contrib.auth.models import User



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

class MessageForm(Form):
	sender = ModelChoiceField(queryset=MailAccount.objects.none())
	recipient = EmailField(required=True)
	subject = CharField(required=False)
	body = CharField(required=False, widget=Textarea)


	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		super(MessageForm, self).__init__(*args, **kwargs)
		usero = User.objects.get(username__exact=user)
		self.fields['sender'].queryset = MailAccount.objects.filter(mail_account_owner=usero)
