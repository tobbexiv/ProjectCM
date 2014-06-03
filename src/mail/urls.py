from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'mail.views.mailaccount_list', name='mailaccount_list'),
	url(r'^view/(?P<pk>\d+)$', 'mail.views.mailaccount_view', name='mailaccount_view'),
	url(r'^new$', 'mail.views.mailaccount_create', name='mailaccount_new'),
	url(r'^delete/(?P<pk>\d+)$', 'mail.views.mailaccount_delete', name='mailaccount_delete'),
)
