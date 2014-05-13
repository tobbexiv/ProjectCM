from django.conf.urls import patterns, url


urlpatterns = patterns('', 
	url(r'^$', 'accounts.views.account_show', name='account_show'),
	url(r'^edit/(?P<pk>\d+)$', 'accounts.views.account_edit', name='account_edit'),
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^register/$', RegistrationViewUniqueEmail.as_view(), name='registration_register'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page' : 'projectcm.views.home'}), 
	url(r'^password/change/$', 'django.contrib.auth.views.password_change', name='password_change'),
	url(r'^password/change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
)
# registration.backends.default.urls