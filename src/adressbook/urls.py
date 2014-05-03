from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'adressbook.views.adress_list', name='adress_list'),
  	url(r'^new$', 'adressbook.views.adress_create', name='adress_new'),
  	url(r'^edit/(?P<pk>\d+)$', 'adressbook.views.adress_update', name='adress_edit'),
  	url(r'^delete/(?P<pk>\d+)$', 'adressbook.views.adress_delete', name='adress_delete'),
)
