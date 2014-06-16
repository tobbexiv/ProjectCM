from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.static import *



admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'projectcm.views.home', name='home'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^adressbook/', include('adressbook.urls')),
	url(r'^account/', include('account.urls')),
	url(r'^mail/', include('mail.urls')),
	url(r'^calendar/', include('cal.urls')),
	(r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
	
