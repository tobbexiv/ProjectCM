from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from mail.models import MailAccount, MailHost
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
	send_host = MailHost.objects.get(send_host_of=account.send_host)
	# retrieve_host = MailHost.objects.get(retrieve_host_of=account.retrieve_host)	

	data = {}
	data['account'] = account
	data['send_host'] = send_host
	# data['retrieve_host'] = retrieve_host

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


	