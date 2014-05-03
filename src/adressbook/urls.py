from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'adressbook.views.home', name='home'),
)
