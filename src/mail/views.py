from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from mail.models import MailAccount, MailHost


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
	retrieve_host = MailHost.objects.get(retrieve_host_of=account.retrieve_host)	

	data = {}
	data['account'] = account
	data['send_host'] = send_host
	data['retrieve_host'] = retrieve_host

	return render(request, template_name, data)