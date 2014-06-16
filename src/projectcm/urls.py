from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.static import *



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'projectcm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^$', 'projectcm.views.home', name='home'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^adressbook/', include('adressbook.urls')),	
	url(r'^accounts/', include('allauth.urls')),
	url(r'^accounts/', include('accounts.urls')),
	url(r'^mail/', include('mail.urls')),
	# url(r'^accounts/', include('registration.backends.default.urls')),
	(r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
	
