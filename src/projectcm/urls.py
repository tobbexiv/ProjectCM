from django.conf.urls import patterns, include, url

from django.contrib import admin



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'projectcm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^$', 'projectcm.views.home', name='home'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^adressbook/', include('adressbook.urls')),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page' : 'projectcm.views.home'}), 
	url(r'^accounts/password/change/$', 'django.contrib.auth.views.password_change', name='password_change'),
	url(r'^accounts/password/change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
	url(r'^userdata/', include('userdata.urls')),
)
