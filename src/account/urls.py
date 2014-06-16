from django.conf.urls import patterns, url


urlpatterns = patterns('', 
	url(r'^$', 'account.views.account_show'),
	url(r'^edit/(?P<pk>\d+)$', 'account.views.account_edit', name='account_edit'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'account/login.html'}),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page' : 'projectcm.views.home'}), 
	#url(r'^register/$', 'accounts.forms.RegistrationView.as_view()', name='registration_register'),
	
	url(r'^password/change/$', 'django.contrib.auth.views.password_change', name='password_change'),
	url(r'^password/change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
)
# registration.backends.default.urls
