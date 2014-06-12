from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'adressbook.views.adress_list', name='adress_list'),
	url(r'^new$', 'adressbook.views.adress_new', name='adress_new'),
	url(r'^view/(?P<pk>\d+)$', 'adressbook.views.adress_view', name='adress_view'),
	url(r'^edit/(?P<pk>\d+)$', 'adressbook.views.adress_edit', name='adress_edit'),
	url(r'^delete/(?P<pk>\d+)$', 'adressbook.views.adress_delete', name='adress_delete'),
)
