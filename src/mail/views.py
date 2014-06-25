from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core import serializers

from django.http import HttpResponse
from mail.imap_helper import ImapHelper
from mail.smtp_helper import SmtpHelper
from django.forms.models import model_to_dict
import json
from mail.models import MailAccount, MailHost, Message, MailBox
from mail.forms import MailAccountForm, MailHostForm

from mail.serializer import AccountSerializer 

from django.core.exceptions import ObjectDoesNotExist

@login_required
def mailaccount_list(request, template_name='mail/mailaccount_list.html'):
	accounts = MailAccount.objects.filter(mail_account_owner=request.user)	

	data = {}
	data['object_list'] = accounts

	return render(request, template_name, data)


@login_required
def mailaccount_view(request, pk, template_name='mail/mailaccount_view.html'):
	account = MailAccount.objects.get(pk=pk)
	send_host = MailHost.objects.get(pk=account.send_host.id)
	retrieve_host = MailHost.objects.get(pk=account.retrieve_host.id)	

	data = {}
	data['account'] = account
	data['send_host'] = send_host
	data['retrieve_host'] = retrieve_host

	return render(request, template_name, data)


@login_required
def mailaccount_new(request, template_name='mail/mailaccount_form.html'):
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
def mailaccount_delete(request, pk, template_name='mail/mailaccount_delete.html'):
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
def mailaccount_edit(request, pk, template_name='mail/mailaccount_form.html'):
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
def mailaccount_select(request, template_name='mail/mailaccount_select.html'):
	accounts = MailAccount.objects.filter(mail_account_owner=request.user)	
	data = {}
	data['title'] = "Select Mail Account"
	data['object_list'] = accounts

	return render(request, template_name, data)

@login_required
def mailboxes_list(request, mail_account_id):
	mail_account = MailAccount.objects.get(pk=mail_account_id)
	imap_helper = ImapHelper(mail_account)
	mailboxes_server = imap_helper.load_mailboxes()

	for mb in mailboxes_server:
		if not MailBox.objects.filter(name=str(mb), mail_account=mail_account):
			m = MailBox(name=str(mb), mail_account=mail_account)
			m.save()
			
	
	mailboxes_local = MailBox.objects.filter(mail_account=mail_account)
	json_data = serializers.serialize('json', mailboxes_local)

	return HttpResponse(json_data, content_type="application/json") 


@login_required
def message_list(request, pk, template_name='mail/message_list.html'):
	account_data = MailAccount.objects.get(pk=pk)
	
	imap_helper = ImapHelper(account_data)
	data = {}
	data['account'] = str(account_data)

	mailbox = request.GET.get('mailbox', False)
	if mailbox is not False:
		imap_helper.select_mailbox(mailbox)
	else:
		imap_helper.select_mailbox('INBOX')
		mailbox = 'INBOX'

	try:
		mb = MailBox.objects.get(mail_account=account_data.id, name=mailbox)
	except ObjectDoesNotExist:
			mb = MailBox(name=str(mailbox), mail_account=account_data)
			mb.save()


	messages = imap_helper.load_mail_from_mailbox()
	print(messages)

	for message in messages:		
		
		check = Message.objects.filter(identifier=message['identifier'], mail_box=mb)
		
		if not check:
			m = Message(mail_box=mb, sender=message['sender'], subject=message['subject'], identifier=message['identifier'], mail_source=message['source'])
			m.save()

	ms = Message.objects.filter(mail_box=mb)

	data['object_list'] = ms

	return render(request, template_name, data)


@login_required
def message_view(request, pk, template_name='mail/message_view.html'):
	message = Message.objects.get(pk=pk)
	data = {}
	data['message'] = message 

	return render(request, template_name, data)


@login_required
def message_send(request):
	if request.method == "POST" and request.is_ajax: 
		json_data = json.loads(request.body.decode('utf-8'))
		account_id = json_data['account']
		recipient = json_data['recipient']
		body = json_data['body']

		account_data = MailAccount.objects.get(pk=account_id)
		smtp_helper = SmtpHelper(account_data)
		sender = account_data.email

		message = {}
		mail['sender'] = sender
		mail['destination'] = recipient
		msg = ("From: %s\r\nTo: %s\r\n\r\n"
       % (fromaddr, ", ".join(toaddrs.split())))
		mail['body'] = msg + body

		smtp_helper.send_message(mail)

		return HttpResponse("message send")	

