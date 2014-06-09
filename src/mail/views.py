from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core import serializers


from django.http import HttpResponse
from mail.imap_helper import ImapHelper
from django.forms.models import model_to_dict

from mail.models import MailAccount, MailHost, Message
from mail.forms import MailAccountForm, MailHostForm

@login_required
def mailaccount_list(request, template_name='mailaccount_list.html'):
	accounts = MailAccount.objects.filter(mail_account_owner=request.user)	
	data = {}
	data['title'] = "Mail Accounts"
	data['object_list'] = accounts

	return render(request, template_name, data)


@login_required
def mailaccount_view(request, pk, template_name='mailaccount_view.html'):
	account = MailAccount.objects.get(pk=pk)
	send_host = MailHost.objects.get(pk=account.send_host.id)
	retrieve_host = MailHost.objects.get(pk=account.retrieve_host.id)	

	data = {}
	data['account'] = account
	data['send_host'] = send_host
	data['retrieve_host'] = retrieve_host

	return render(request, template_name, data)


@login_required
def mailaccount_create(request, template_name='mailaccount_form.html'):
	mailaccount_form = MailAccountForm(request.POST or None)
	mailhost_send_form = MailHostForm(request.POST or None, prefix='send')
	mailhost_retrieve_form = MailHostForm(request.POST or None, prefix='retrieve')

	if mailaccount_form.is_valid() and mailhost_send_form.is_valid() and mailhost_retrieve_form.is_valid():

		send_host = mailhost_send_form.save()
		retrieve_host = mailhost_retrieve_form.save()

		account = mailaccount_form.save(commit=False)
		account.mail_account_owner = request.user
		account.retrieve_host = retrieve_host
		account.send_host = send_host		
		account.save()		


		return redirect('mailaccount_view', pk=account.id)

	data = {}
	data['mailaccount'] = mailaccount_form
	data['send_host'] = mailhost_send_form
	data['retrieve_host'] = mailhost_retrieve_form

	return render(request, template_name, data)


@login_required
def mailaccount_delete(request, pk, template_name='mailaccount_delete.html'):
	account = get_object_or_404(MailAccount, pk=pk)
	retrieve_host = get_object_or_404(MailHost, retrieve_host_of=account)
	send_host = get_object_or_404(MailHost, send_host_of=account)

	if request.method=='POST':
		account.delete()
		retrieve_host.delete()
		send_host.delete()
		return redirect('mailaccount_list')

	return render(request, template_name, {'object':account})	


@login_required
def mailaccount_update(request, pk, template_name='mailaccount_form.html'):
	account = get_object_or_404(MailAccount, pk=pk)
	retrieve_host = get_object_or_404(MailHost, retrieve_host_of=account)
	send_host = get_object_or_404(MailHost, send_host_of=account)

	mailaccount_form = MailAccountForm(request.POST or None, instance=account)
	mailhost_send_form = MailHostForm(request.POST or None, prefix='send', instance=send_host)
	mailhost_retrieve_form = MailHostForm(request.POST or None, prefix='retrieve', instance=retrieve_host)

	if mailaccount_form.is_valid() and mailhost_send_form.is_valid() and mailhost_retrieve_form.is_valid():

		send_host = mailhost_send_form.save()
		retrieve_host = mailhost_retrieve_form.save()

		account = mailaccount_form.save(commit=False)
		account.mail_account_owner = request.user
		account.retrieve_host = retrieve_host
		account.send_host = send_host		
		account.save()		


		return redirect('mailaccount_view', pk=account.id)

	data = {}
	data['mailaccount'] = mailaccount_form
	data['send_host'] = mailhost_send_form
	data['retrieve_host'] = mailhost_retrieve_form

	return render(request, template_name, data)


@login_required
def select_mailaccount(request, template_name='select_mailaccount.html'):
	accounts = MailAccount.objects.filter(mail_account_owner=request.user)	
	data = {}
	data['title'] = "Select Mail Account"
	data['object_list'] = accounts

	return render(request, template_name, data)

@login_required
def mailboxes_list(request, mail_account_id):
	mail_account = MailAccount.objects.get(mail_account_owner=request.user, pk=mail_account_id)
	imap_helper = ImapHelper(mail_account)
	mailboxes = imap_helper.load_mailboxes()

	json_data = serializers.serialize('json', [ mail_account, ])

	return HttpResponse(json_data, mimetype="application/json") 


@login_required
def message_list(request, pk, template_name='message_list.html'):
	account_data = MailAccount.objects.get(pk=pk)
	
	imap_helper = ImapHelper(account_data)
	data = {}
	data['account'] = str(account_data)
	imap_helper.select_mailbox('inbox')

	messages = imap_helper.load_mail_from_mailbox()

	for message in messages:
		m = Message(mail_account=account_data, mail_source=message)
		m.save()

	ms = Message.objects.filter(mail_account=account_data)

	data['object_list'] = ms

	return render(request, template_name, data)