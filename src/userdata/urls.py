from django.conf.urls import patterns, url

urlpatterns = patterns('', 
	url(r'^$', 'userdata.views.userdata_show', name='userdata_show'),
	url(r'^edit/(?P<pk>\d+)$', 'userdata.views.userdata_edit', name='userdata_edit'),
	
)