from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'mail.views.mailaccount_list', name='mailaccount_list'),
	url(r'^view/(?P<pk>\d+)$', 'mail.views.mailaccount_view', name='mailaccount_view'),
	url(r'^new$', 'mail.views.mailaccount_create', name='mailaccount_new'),
	url(r'^delete/(?P<pk>\d+)$', 'mail.views.mailaccount_delete', name='mailaccount_delete'),
	url(r'^edit/(?P<pk>\d+)$', 'mail.views.mailaccount_update', name='mailaccount_update'),

	url(r'^select/$', 'mail.views.select_mailaccount', name='select_mailaccount'),
	url(r'^message/list/(?P<pk>\d+)$', 'mail.views.message_list', name='message_list'),
	url(r'^mailboxes/list/(?P<mail_account_id>\d+)$', 'mail.views.mailboxes_list', name='mailboxes_list'),

	url(r'^messages/view/(P<pk>\d+)$', 'mail.views.message_view', name='message_view'),
)
